#!/usr/bin/env python3
"""
NetWatch - ICMP Latency + Uptime Monitor (Cross-platform)

USAGE EXAMPLES:
    netwatch -f targets.txt -i 30 -o icmp_log.csv
    netwatch --targets 8.8.8.8 192.168.1.1 -i 15

Arguments:
    -f, --file       File with targets (one per line)
    --targets        IPs or domains passed directly (optional)
    -i, --interval   Ping interval in seconds (default: 30)
    -o, --output     Output CSV file (default: icmp_log.csv)

Dependencies:
    pip install colorama

Tested on Windows, Linux, macOS
"""

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
# Ping a single host (cross-platform)
# -------------------------------
def ping_host(host):
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", "2000", host]
    else:
        cmd = ["ping", "-c", "1", "-W", "2", host]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "time=" in line.lower():
                    # Handle both Linux and Windows latency format
                    try:
                        latency = line.lower().split("time=")[-1].split("ms")[0].strip()
                        return "UP", latency
                    except:
                        return "UP", "Unknown"
        return "DOWN", "Timeout"
    except Exception:
        return "DOWN", "Error"

# -------------------------------
# Load from file
# -------------------------------
def load_targets_from_file(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("# Add one IP or domain per line\n")
        print(Fore.YELLOW + f"[+] Created empty file: {file}")
        print(Fore.CYAN + "[!] Add targets and re-run, or use --targets.")
        return []
    
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

# -------------------------------
# Log to CSV
# -------------------------------
def log_result(file, row):
    file_exists = os.path.isfile(file)
    with open(file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Host", "Status", "Latency (ms)"])
        writer.writerow(row)

# -------------------------------
# Main loop
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="Cross-platform ICMP Monitor")
    parser.add_argument("-f", "--file", help="Target file")
    parser.add_argument("--targets", nargs="*", help="Targets passed directly")
    parser.add_argument("-i", "--interval", type=int, default=30, help="Interval (sec)")
    parser.add_argument("-o", "--output", default="icmp_log.csv", help="CSV output")

    args = parser.parse_args()

    file_targets = load_targets_from_file(args.file) if args.file else []
    cli_targets = args.targets if args.targets else []
    targets = list(set(file_targets + cli_targets))

    if not targets:
        print(Fore.RED + "[-] No targets provided. Use -f or --targets.")
        return

    print(Fore.CYAN + f"[+] Monitoring {len(targets)} targets every {args.interval}s. Output: {args.output}")

    try:
        while True:
            print(Fore.BLUE + f"\n[{datetime.now().strftime('%H:%M:%S')}] Running checks...")
            for host in targets:
                status, latency = ping_host(host)
                log_result(args.output, [datetime.now().isoformat(), host, status, latency])
                if status == "UP":
                    print(Fore.GREEN + f"[+] {host} is UP - {latency} ms")
                else:
                    print(Fore.RED + f"[-] {host} is DOWN - {latency}")
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Monitor stopped by user.")

# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    main()
