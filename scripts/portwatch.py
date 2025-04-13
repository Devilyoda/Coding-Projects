#!/usr/bin/env python3
"""
PortWatch - Live Port Change Detection (Cross-Platform)

Scans a host or subnet and compares open ports to a saved baseline.
Detects:
- New open ports (not in baseline)
- Closed ports (were open, now closed)

Features:
- Threaded scanning
- Full port or custom port range
- Auto-creates baseline JSON if missing
- Optional CSV/JSON diff log output
- Works on Windows, Linux, macOS

USAGE EXAMPLES:
    portwatch 192.168.1.1 -p 1-1000
    portwatch 192.168.1.1 -p 22,80 -b my_baseline.json -o port_diff.csv --save-new

Arguments:
    target              Target IP or hostname
    -p, --ports         Ports or ranges (e.g. 22,80,1000-1100)
    -b, --baseline      Baseline JSON file (default: portwatch_baseline.json)
    -o, --output        Output CSV file (optional)
    -t, --threads       Thread count (default: 100)
    --save-new          Overwrite baseline with current state after scan

Dependencies:
    pip install colorama tqdm

Notes for Windows Users:
- This script does not read Windows Event Viewer directly.
- To analyze Event Logs:
    1. Open Event Viewer → Export as .txt or .log
    2. Use this exported file with tools like `logwatch.py`
    3. You can also convert .evtx to text with third-party tools
"""

import socket
import argparse
import json
import os
import csv
from tqdm import tqdm
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

# -------------------------------
# Parse ports
# -------------------------------
def parse_ports(port_str):
    ports = set()
    for part in port_str.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part.strip()))
    return sorted(ports)

# -------------------------------
# Scan single port
# -------------------------------
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return port
    except:
        pass
    return None

# -------------------------------
# Main logic
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="Live Port Change Watcher")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", help="Ports or ranges (e.g. 22,80,1000-2000)", required=True)
    parser.add_argument("-b", "--baseline", help="Baseline file (default: portwatch_baseline.json)", default="portwatch_baseline.json")
    parser.add_argument("-o", "--output", help="CSV diff output file (optional)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Thread count")
    parser.add_argument("--save-new", action="store_true", help="Overwrite baseline with new scan")
    args = parser.parse_args()

    ports = parse_ports(args.ports)
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(Fore.RED + f"[-] Could not resolve target: {args.target}")
        return

    print(Fore.CYAN + f"[+] Scanning {args.target} on {len(ports)} ports...")
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in ports}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning", ncols=80):
            result = future.result()
            if result:
                open_ports.append(result)

    open_ports = sorted(open_ports)
    print(Fore.GREEN + f"[+] Found {len(open_ports)} open ports.")

    # Load baseline
    if os.path.exists(args.baseline):
        with open(args.baseline, "r") as f:
            baseline_data = json.load(f)
    else:
        baseline_data = {}

    previous_ports = baseline_data.get(args.target, [])
    current_set = set(open_ports)
    previous_set = set(previous_ports)

    new_ports = sorted(list(current_set - previous_set))
    closed_ports = sorted(list(previous_set - current_set))

    print(Fore.YELLOW + f"[+] New open ports: {new_ports if new_ports else 'None'}")
    print(Fore.MAGENTA + f"[+] Closed ports: {closed_ports if closed_ports else 'None'}")

    # Save diff to CSV if requested
    if args.output:
        try:
            with open(args.output, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Change Type", "Port"])
                for p in new_ports:
                    writer.writerow(["NEW", p])
                for p in closed_ports:
                    writer.writerow(["CLOSED", p])
            print(Fore.YELLOW + f"[+] Diff saved to: {os.path.abspath(args.output)}")
        except Exception as e:
            print(Fore.RED + f"[-] Failed to save output: {e}")

    # Update baseline if requested
    if args.save_new:
        baseline_data[args.target] = open_ports
        with open(args.baseline, "w") as f:
            json.dump(baseline_data, f, indent=4)
        print(Fore.CYAN + f"[+] Baseline updated: {args.baseline}")
    elif not os.path.exists(args.baseline):
        print(Fore.YELLOW + f"[!] No baseline found. Creating new baseline file.")
        baseline_data[args.target] = open_ports
        with open(args.baseline, "w") as f:
            json.dump(baseline_data, f, indent=4)
        print(Fore.CYAN + f"[+] Baseline saved: {args.baseline}")

if __name__ == "__main__":
    main()
