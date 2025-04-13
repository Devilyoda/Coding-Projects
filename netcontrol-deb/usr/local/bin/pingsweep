#!/usr/bin/env python3
"""
Ping Sweep Script (Cross-Platform)

Performs a multithreaded ping sweep over a given subnet.
Features:
- Threading for speed
- Hostname resolution
- Color-coded terminal output
- CSV output with headers
- Logging to timestamped log file
- Auto-opens results after scan
- Works on Linux, Windows, and macOS

USAGE EXAMPLE:
    python3 pingsweep.py 192.168.1.0/24 -o live_hosts.csv -t 100

Arguments:
    subnet         The subnet to scan (CIDR notation)
    -o, --output   Output CSV file name (optional)
    -t, --threads  Number of concurrent threads (optional, default=100)

Dependencies:
    pip install colorama tqdm

Tested on Ubuntu, Windows, and macOS.
"""

import ipaddress
import subprocess
import socket
import argparse
import csv
import logging
import os
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import Fore, init
from datetime import datetime

# Init colorama
init(autoreset=True)

# -------------------------------
# Function: Setup logging
# -------------------------------
def setup_logger():
    log_filename = f"pingsweep_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return log_filename

# -------------------------------
# Function: Ping a single IP address (cross-platform)
# -------------------------------
def ping_host(ip):
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", "1000", str(ip)]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", str(ip)]

    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            try:
                hostname = socket.gethostbyaddr(str(ip))[0]
            except socket.herror:
                hostname = "Unknown"
            return f"{ip},{hostname}"
    except Exception:
        pass
    return None

# -------------------------------
# Main Execution Logic
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="Ping Sweep Tool (Cross-Platform)")
    parser.add_argument("subnet", help="Target subnet (e.g., 192.168.1.0/24)")
    parser.add_argument("-o", "--output", help="Output CSV file (e.g., live_hosts.csv)", default=None)
    parser.add_argument("-t", "--threads", help="Number of threads (default: 100)", type=int, default=100)

    args = parser.parse_args()
    log_file = setup_logger()

    try:
        ip_net = ipaddress.ip_network(args.subnet, strict=False)
        all_hosts = list(ip_net.hosts())
    except ValueError as e:
        print(f"{Fore.RED}[-] Invalid subnet: {e}")
        logging.error(f"Invalid subnet: {e}")
        return

    print(f"{Fore.CYAN}[+] Starting ping sweep on subnet {args.subnet} with {args.threads} threads...\n")
    logging.info(f"Started scan on {args.subnet} with {args.threads} threads.")

    live_hosts = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(ping_host, ip): ip for ip in all_hosts}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning", ncols=80):
            result = future.result()
            if result:
                ip, hostname = result.split(",")
                print(Fore.GREEN + f"[+] {ip} is up ({hostname})")
                live_hosts.append((ip, hostname))

    if args.output:
        try:
            output_path = os.path.abspath(args.output)
            with open(output_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["IP", "Hostname"])
                for ip, hostname in live_hosts:
                    writer.writerow([ip, hostname])
            print(f"\n{Fore.YELLOW}[+] Results saved to: {output_path}")
            logging.info(f"Results saved to: {output_path}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to write output file: {e}")
            logging.error(f"Failed to write output file: {e}")

    print(f"\n{Fore.CYAN}[+] Scan complete. {len(live_hosts)} live hosts found.")
    logging.info(f"Scan complete. {len(live_hosts)} live hosts found.")
    logging.info(f"Log file saved as: {log_file}")

    # Auto-open CSV (Linux/mac only)
    if args.output and platform.system().lower() != "windows":
        try:
            subprocess.Popen(["xdg-open", output_path])
            logging.info(f"Opened CSV file: {output_path}")
        except Exception as e:
            print(f"{Fore.RED}[-] Could not open CSV file: {e}")
            logging.warning(f"Could not open CSV file: {e}")

    # Auto-open log file (Linux/mac only)
    if platform.system().lower() != "windows":
        try:
            subprocess.Popen(["xdg-open", log_file])
            logging.info(f"Opened log file: {log_file}")
        except Exception as e:
            print(f"{Fore.RED}[-] Could not open log file: {e}")
            logging.warning(f"Could not open log file: {e}")

# -------------------------------
# Script Entry Point
# -------------------------------
if __name__ == "__main__":
    main()
