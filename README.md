# ⚡ NetProbe v2.0  
_A Lightweight Network Utility Tool_ 

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

---

## 📌 Overview
**NetProbe v2.0** is a command-line based network utility built with Python.  
It provides essential **network reconnaissance tools** such as:

- 🔍 **Port Scanning** – Identify open ports on a target host with multi-threaded execution.  
- 🌐 **Hostname Resolution** – Quickly resolve domain names to IP addresses.  
- 🔗 **Connectivity Testing** – Test basic network connectivity to hosts.
- ⚙️ **Multi-threaded Execution** – Faster scanning with configurable thread pools.
- 🛡️ **Security Features** – Built-in validation to prevent scanning of localhost/private networks.

⚠️ **Disclaimer**: This project is created for **educational and research purposes only**.  
You are responsible for using it **legally and ethically** on systems you own or have explicit permission to test.  

---

## 🚀 Features
- ✅ Multi-threaded port scanner (fast & efficient).  
- ✅ Target hostname/IP resolution with validation.  
- ✅ Basic connectivity testing.
- ✅ Command-line interface with argument support.
- ✅ Interactive menu mode.
- ✅ Colored console output using `colorama`.  
- ✅ Clean and modular code structure.
- ✅ Security safeguards against scanning localhost/private networks.

---

## 📦 Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/ahmed-gocode/NetProbe.git
cd NetProbe
pip install -r requirements.txt
```

## 💻 Usage

### Command Line Mode
```bash
# Port scan a target
python netprobe.py --scan example.com --ports 1000 --threads 50

# Resolve hostname
python netprobe.py --resolve example.com

# Test connectivity
python netprobe.py --ping example.com

# Interactive mode
python netprobe.py --interactive
```

### Interactive Mode
Simply run the script without arguments for the interactive menu:
```bash
python netprobe.py
```

### Command Line Options
- `--scan, -s`: Target hostname or IP to scan
- `--ports, -p`: Port range to scan (1 to N, default: 1000)
- `--threads, -t`: Number of threads (default: 50, max: 200)
- `--resolve, -r`: Resolve hostname to IP address
- `--ping`: Test connectivity to a host
- `--interactive, -i`: Run in interactive mode
- `--help, -h`: Show help message

---

## 🛡️ Security & Ethics

This tool includes built-in safety features:
- Prevents scanning of localhost (127.0.0.1, ::1)
- Warns against scanning private IP ranges (10.x.x.x, 172.16.x.x, 192.168.x.x)
- Limits thread count to prevent system overload
- Validates all user inputs

**Important**: 
- Do NOT use this tool to scan systems without authorization
- Always respect rate limits and terms of service
- The author is not responsible for misuse of this software
- This tool is for educational and authorized testing purposes only

---
<p align="center">Made with ❤️ by Ahmad</p>
