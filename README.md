# rtsp-bruteforce-script
![image alt](https://github.com/AbdulRaheem785/rtsp-bruteforce-script/blob/91fc72c43d45cefee29c08038fc042ce36722197/R4HIM-0xBRUTE.png)

By AbdulRaheem Butt

A high‑performance, multi‑threaded Python tool for auditing RTSP streams on IP cameras, DVR/NVRs, baby monitors, and IoT video devices.

R4H1M‑0xBRUTE can attack weak and strong credentials, supports huge wordlists like rockyou.txt, and performs vendor‑specific RTSP path discovery, including Dahua, Hikvision, 

XMeye, and generic ONVIF-based cameras.
**⚡ Key Features**

**🔐 Credential Bruteforce**

Supports both username:password combo lists and separate username/password lists

Designed for large dictionaries (rockyou, leak-dumps, custom lists)


**🎥 RTSP Path Discovery**

_Automatically scans:_

✔ Common camera RTSP paths

✔ User-defined paths from Lib/path.txt

✔ Vendor-specific paths (Dahua included)

Helps locate hidden, undocumented, or manufacturer-only stream paths

**🧠 Vendor Support**

Works with Dahua, Hikvision, XMeye, Uniview, ONVIF, and most generic RTSP devices

Includes Dahua stale‑nonce fix for accurate authentication handling

**🚀 Optimized Multithreading**

Smart, dynamic thread pool for extremely fast attack performance

Handles thousands of concurrent requests without freezing or CPU overload

**🛠️ Installation**

git clone https://github.com/AbdulRaheem785/rtsp-bruteforce-script.git

cd rtsp-bruteforce-script

cd R4H1M‑0xBRUTE

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

**Run the script:**

python3 rtsp.py
