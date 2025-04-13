# NetControl

**NetControl** is a unified command-line interface for launching and managing network/security automation tools. It was built to simplify scanning, monitoring, and log analysis in real-world IT and cybersecurity environments.

Created by **Chris Giggleman** under the **Devilyoda Products** brand.

---

## 🚀 Features

- Centralized controller for:
  - ✅ Ping Sweep
  - ✅ Port Scanner
  - ✅ Network Watcher (Uptime + Baseline tracking)
  - ✅ Service Watch (host:port availability)
  - ✅ Log Watch (filter and monitor logs)
- Interactive menu UI
- CLI arguments support for automation
- Run all tools in sequence
- Colorized output with `rich`
- Timeout support for long-running monitors

---

## 🛠 Installation

1. **Place all scripts** in a project folder (e.g., `~/Documents/Scripts`).
2. **Make each script executable**:
   ```bash
   chmod +x script_name.py

Move them to a global path (e.g., /usr/local/bin) and rename:
sudo mv ping_sweep.py /usr/local/bin/pingsweep
sudo mv port_scanner.py /usr/local/bin/portscan
sudo mv netwatch.py /usr/local/bin/netwatch
sudo mv servwatch.py /usr/local/bin/servwatch
sudo mv logwatch.py /usr/local/bin/logwatch
sudo mv netcontrol.py /usr/local/bin/netcontrol

Run from anywhere:
netcontrol

📋 Script Usage Examples
🔹 Pingsweep
Discover live hosts on a subnet.
pingsweep 192.168.1.0/24 -t 100 -o live_hosts.csv
🔹 Portscan

Scan for open ports and services.
portscan -f targets.txt -o results.csv -p 22,80,443 -t 50
🔹 Netwatch

Monitor host uptime on a schedule.
netwatch -f targets.txt -o netwatch_log.csv --interval 60 -t 50 --baseline
🔹 Servwatch

Check TCP port status on services.
servwatch -f services.txt -o service_log.csv --interval 30
🔹 Logwatch

Track logs with filters and regex.
logwatch -f /var/log/syslog --filter DROP --output blocked.csv

🔧 Running the Controller
netcontrol

This will launch the interactive dashboard:
======= NetControl Menu =======
1. Ping Sweep
2. Port Scanner
3. Net Watch
4. Service Watch
5. Log Watch
6. Run All
0. Exit

CLI options:
netcontrol --tool portscan --args "-f targets.txt -o result.csv"
netcontrol --run-all

📁 Input Files
targets.txt: List of IPs for scanning/monitoring
services.txt: Format host:port, one per line

🧠 About the Creator
Chris Giggleman is an IT professional with a passion for automation and security. His brand Devilyoda Products focuses on practical tools for IT professionals and cybersecurity teams.
