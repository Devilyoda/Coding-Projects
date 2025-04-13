# NetControl

![NetControl Logo](https://img.shields.io/badge/Devilyoda-Tool-green?style=for-the-badge)
[![GitHub Release](https://img.shields.io/github/v/release/devilyoda/netcontrol?style=flat-square)](https://github.com/devilyoda/Coding-Projects/releases)
[![License](https://img.shields.io/github/license/devilyoda/netcontrol?style=flat-square)](./LICENSE)

**NetControl** is a master network operations controller for launching and managing all your custom Python-based network scripts from a single interface.

Developed by **Chris Giggleman** for [Devilyoda Products](https://github.com/devilyoda).

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
sudo cp Scripts/pingsweep.py /usr/local/bin/pingsweep
sudo chmod +x /usr/local/bin/pingsweep
# Repeat for all scripts:
sudo cp Scripts/portscan.py /usr/local/bin/portscan
sudo cp Scripts/netwatch.py /usr/local/bin/netwatch
sudo cp Scripts/servwatch.py /usr/local/bin/servwatch
sudo cp Scripts/logwatch.py /usr/local/bin/logwatch
sudo cp netcontrol.py /usr/local/bin/netcontrol
sudo chmod +x /usr/local/bin/*
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

## 📸 Screenshots (Optional)

| Master Menu | Ping Sweep | Port Scan |
|-------------|------------|-----------|
| ![Menu](https://via.placeholder.com/300x150?text=Main+Menu) | ![Ping](https://via.placeholder.com/300x150?text=Ping+Sweep) | ![Port](https://via.placeholder.com/300x150?text=Port+Scan) |

---

## 🤝 Contributing

Got improvements or issues? [Open an Issue](https://github.com/devilyoda/netcontrol/issues) or submit a pull request!

---

## 🔐 GPG + SSH Key Authentication

To push securely using GitHub CLI or terminal:

```bash
# Set global identity
git config --global user.name "Chris Giggleman"
git config --global user.email "your_email@example.com"

# Generate SSH key (optional)
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub  # Add this to GitHub under SSH keys

# Or use a Personal Access Token (PAT)
# Copy from GitHub → Settings → Developer Settings → Tokens → Generate new token (Classic)
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
