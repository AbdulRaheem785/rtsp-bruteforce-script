# rtsp-bruteforce-script
![image alt](https://github.com/AbdulRaheem785/rtsp-bruteforce-script/blob/91fc72c43d45cefee29c08038fc042ce36722197/R4HIM-0xBRUTE.png)
Advanced Multithreaded RTSP Bruteforce &amp; Path Discovery Tool BY ABDULRAHEEM BUTT

A simple, multi‑threaded Python tool that bruteforces RTSP credentials and RTSP stream paths on IP cameras, DVR/NVRs, and IoT video devices.

This tool attempts to authenticate using a list of username:password pairs, and checks multiple RTSP paths (both built‑in common camera paths and user‑supplied paths from path.txt).
If valid credentials and a valid RTSP stream path are found, the tool immediately prints the result and stops.

🛠️ Installation

git clone https://github.com/AbdulRaheem785/rtsp-bruteforce-script.git

cd rtsp-bruteforce-script

cd R4H1M‑0xBRUTE

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

**Run the script:**

python3 rtsp.py
