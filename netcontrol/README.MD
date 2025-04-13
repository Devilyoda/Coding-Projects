# NetControl

![NetControl Logo](https://img.shields.io/badge/Devilyoda-Tool-green?style=for-the-badge)

**NetControl** is a master network operations controller for launching and managing all your custom Python-based network scripts from a single interface.

Developed with ❤️ by **Chris Giggleman** for [Devilyoda Products](https://github.com/devilyoda).

---

## 📦 Features
- Centralized interface for:
  - Ping sweeps
  - Port scanning
  - Network uptime monitoring
  - Service health checks
  - Log file watching
- Custom presets & CLI arguments
- Real-time TUI (using `rich`)
- Designed for Linux environments
- Installable as a `.deb` package

---

## 📂 Project Structure
```
netcontrol/
├── netcontrol.py                 # Launcher script
├── netcontrol_1.1_all.deb       # Installable package (optional in GitHub repo)
├── netcontrol-deb/              # Debian packaging folder
│   ├── DEBIAN/
│   │   ├── control
│   │   ├── postinst
│   │   └── prerm
│   └── usr/
│       └── local/
│           └── bin/
│               ├── netcontrol
│               ├── pingsweep
│               ├── portscan
│               ├── netwatch
│               ├── servwatch
│               └── logwatch
├── README.md
└── Scripts/                     # Raw Python files
    ├── pingsweep.py
    ├── portscan.py
    ├── netwatch.py
    ├── servwatch.py
    ├── logwatch.py
```

---

## 🚀 Installation

### Option 1: Using the `.deb` Installer

```bash
sudo dpkg -i netcontrol_1.1_all.deb
```

> Make sure dependencies are installed:
```bash
sudo apt install python3-rich python3-commonmark python3-pygments
```

### Option 2: Manual Setup

1. Copy all `Scripts/*.py` files into `/usr/local/bin`.
2. Rename them to match the global commands:

```bash
sudo cp pingsweep.py /usr/local/bin/pingsweep
sudo chmod +x /usr/local/bin/pingsweep
# Repeat for all scripts
```

---

## 🧪 Real-World Usage Examples

### 🔹 Ping Sweep
```bash
pingsweep 192.168.1.0/24 -t 100 -o live_hosts.csv
```

### 🔹 Port Scanner
```bash
portscan -f targets.txt -o portscan.csv -t 100 -p 22,80,443
```

### 🔹 Net Watch
```bash
netwatch -f targets.txt -o netwatch_log.csv --interval 60 --baseline
```

### 🔹 Service Watch
```bash
servwatch -f services.txt -o service_log.csv --interval 30
```

### 🔹 Log Watch
```bash
logwatch -f /var/log/syslog --filter DROP -o alert_log.csv
```

### 🔹 Master Control
```bash
netcontrol                    # Launch the full TUI menu
netcontrol --tool portscan --args "-f targets.txt -o scan.csv"
netcontrol --run-all         # Run all tools in sequence
```

---

## 🔧 Build Your Own .deb Package (Advanced)
To build the `.deb` installer:
```bash
dpkg-deb --build netcontrol-deb netcontrol_1.1_all.deb
```

---

## 📜 License
MIT License © 2024 Chris Giggleman, Devilyoda Products

---

## 🌐 Connect
GitHub: [@devilyoda](https://github.com/devilyoda)  
Twitter/X: [@DevilyodaTech](https://twitter.com/devilyodatech)

---

Happy hacking! 💻🧠

