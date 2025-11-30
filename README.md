# rtsp-bruteforce-script
![image alt](https://github.com/AbdulRaheem785/rtsp-bruteforce-script/blob/91fc72c43d45cefee29c08038fc042ce36722197/R4HIM-0xBRUTE.png)

By AbdulRaheem Butt

A high-performance, multi-threaded Python tool for testing RTSP streams on IP cameras, DVR/NVRs, and IoT video devices.

R4H1M‑0xBRUTE not only attacks weak credentials but also handles large dictionaries (like rockyou.txt) and performs vendor-specific path discovery, including Dahua cameras.

⚡ **Key Features**

🔐 Credential Bruteforce

Supports username:password combos or separate username/password lists

Works with small lists or massive dictionaries (rockyou.txt, etc.)



**RTSP Path Discovery**

Scans multiple RTSP paths automatically:

✔ Common built-in camera paths

✔ User-defined paths from Lib/path.txt

✔ Vendor-specific paths (Dahua-style included)

Helps uncover hidden or undocumented streams

**Vendor Support**

Dahua, Hikvision, XMeye, Uniview, generic ONVIF & RTSP devices

Includes special handling for Dahua stale-nonce authentication

**Optimized Multithreading**

Dynamic thread-pool for high-speed scanning

Prevents CPU spikes while handling thousands of requests concurrently

**🛠️ Installation**

git clone https://github.com/AbdulRaheem785/rtsp-bruteforce-script.git

cd rtsp-bruteforce-script

cd R4H1M‑0xBRUTE

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

**Run the script:**

python3 rtsp.py
