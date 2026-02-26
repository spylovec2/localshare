# localshare
This is a lightweight and efficient file-sharing tool built with FastAPI, designed specifically for sharing files over a local network. It enables users to quickly upload, download, and manage files between devices connected to the same LAN — without relying on external cloud services.

---

## 🚀 Features

- Fast file transfers over local network
- Upload and download support
- Simple and clean REST API
- Lightweight and easy to run
- No internet required
- No application required in receiving device

---

## 🛠 Tech Stack

- Python
- FastAPI
---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/spylovec2/localshare.git
cd ylocalshare
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python localshare.py
```

## ▶️ OR create and install LocalShare.deb file

```bash
chmod +x build_deb.sh
./build_deb.sh
sudo dpkg -i LocalShare.deb
```

Open in your browser:

```
http://localhost:8080
```

---

## 📂 Usage

- Upload files using the upload endpoint.
- Download files using the download endpoint.
- Access from other devices using your local IP:

```
http://YOUR_LOCAL_IP:8080
```

Example:

```
http://192.168.1.10:8080
```

---

## 🎯 Use Cases

- Sharing files between personal devices
- Office LAN file transfer
- Quick file exchange without internet
- Local development environments

---

## 🔒 Note

This tool is intended for **local network usage only**.  
Do not expose it directly to the public internet without proper authentication and security.

---

## 📄 License

MIT License