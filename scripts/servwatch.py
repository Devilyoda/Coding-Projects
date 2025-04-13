#!/usr/bin/env python3
"""
ServWatch - Service Uptime & Port Monitor (Cross-Platform)

Monitors a list of services (IP:Port or Host:Port) for uptime over time.

Features:
- Tracks service availability
- Logs latency in milliseconds
- Saves results to CSV
- Color-coded terminal output
- Auto-creates input file if missing
- Works on Windows, Linux, macOS

USAGE EXAMPLES:
    python3 servwatch.py -f services.txt -i 30 -o service_log.csv

Arguments:
    -f, --file       File with IP:port targets (one per line)
    -i, --interval   Check interval in seconds (default: 30)
    -o, --output     Output CSV file (default: service_log.csv)

Each line in the file must be in the format: IP:PORT or HOSTNAME:PORT

Dependencies:
    pip install colorama

Tested on Windows, Linux, macOS.
"""

import socket
import os
import csv
import time
import argparse
import subprocess
import platform
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

# -------------------------------
# Check if IP:Port is reachable
# -------------------------------
def check_service(ip, port, timeout=2):
    try:
        start = time.time()
        sock = socket.create_connection((ip, port), timeout)
        latency = round((time.time() - start) * 1000, 2)
        sock.close()
        return "UP", latency
    except:
        return "DOWN", "Timeout"

# -------------------------------
# Load services from file
# -------------------------------
def load_services(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("# Example format:\n")
            f.write("192.168.1.1:22\n")
            f.write("example.com:443\n")
        print(Fore.YELLOW + f"[+] Created new file: {filename}")
        print(Fore.CYAN + "[!] Add IP:port entries and re-run.")
        return []
    
    with open(filename, "r") as f:
        services = []
        for line in f:
            if line.strip() and not line.startswith("#"):
                parts = line.strip().split(":")
                if len(parts) == 2:
                    host, port = parts[0].strip(), int(parts[1].strip())
                    services.append((host, port))
        return services

# -------------------------------
# Write result to CSV
# -------------------------------
def log_result(file, row):
    file_exists = os.path.isfile(file)
    with open(file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Host", "Port", "Status", "Latency (ms)"])
        writer.writerow(row)

# -------------------------------
# Main loop
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="Service Uptime Monitor (Cross-Platform)")
    parser.add_argument("-f", "--file", help="Target service file", required=True)
    parser.add_argument("-i", "--interval", type=int, default=30, help="Check interval (seconds)")
    parser.add_argument("-o", "--output", default="service_log.csv", help="CSV output file")

    args = parser.parse_args()
    services = load_services(args.file)

    if not services:
        return

    print(Fore.CYAN + f"[+] Monitoring {len(services)} services every {args.interval}s. Output: {args.output}")

    try:
        while True:
            print(Fore.BLUE + f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking services...")
            for host, port in services:
                status, latency = check_service(host, port)
                log_result(args.output, [datetime.now().isoformat(), host, port, status, latency])

                if status == "UP":
                    print(Fore.GREEN + f"[+] {host}:{port} is UP - {latency} ms")
                else:
                    print(Fore.RED + f"[-] {host}:{port} is DOWN - {latency}")
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Monitor stopped by user.")

    # -------------------------------
    # Optional: auto-open CSV (Linux/macOS only)
    # -------------------------------
    if platform.system().lower() != "windows":
        try:
            subprocess.Popen(["xdg-open", os.path.abspath(args.output)])
        except Exception:
            pass

# -------------------------------
# Script Entry
# -------------------------------
if __name__ == "__main__":
    main()
