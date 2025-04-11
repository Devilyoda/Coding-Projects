#!/usr/bin/env python3
"""
Advanced Multi-Target Port Scanner (Cross-Platform)

Scans one or multiple targets for open TCP ports.
Supports full port range scanning, port lists/ranges, service detection, banner grabbing, CSV output, and filtering.

Features:
- Works on Windows, Linux, macOS
- Custom port lists or full-range
- Banner grabbing + service name
- CSV + logging output
- Auto-generates targets.txt if missing

USAGE EXAMPLES:

    # Scan full TCP port range on multiple targets from a file
    portscan -f targets.txt -o full_report.csv

    # Scan specific ports and port ranges
    portscan -f targets.txt -p 22,80,443,1000-1100 -o scan.csv

    # Filter results to show only banners containing "http"
    portscan -f targets.txt -o scan.csv --filter "http"

    # Optional: Use fast mode (top 1000 ports)
    portscan -f targets.txt --fast -o scan.csv

Arguments:
    -f, --file        File containing list of IPs/hostnames to scan (one per line)
    -p, --ports       Comma-separated list of ports and/or ranges (e.g., 22,80,443,1000-2000)
    -o, --output      Output CSV file (required)
    -t, --threads     Number of threads (default: 100)
    --filter          Keyword to match in banner (optional)
    --fast            Scan only top 1000 ports

Dependencies:
    pip install colorama tqdm

Tested on Windows, Linux, macOS
"""

import socket
import argparse
import csv
import logging
import os
from tqdm import tqdm
from colorama import Fore, init
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

TOP_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
    993, 995, 1723, 3306, 3389, 5900, 8080, 8443
] + list(range(1, 1025))

def setup_logger():
    log_file = f"portscan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Logger initialized")
    return log_file

def parse_ports(port_str):
    ports = set()
    for part in port_str.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part.strip()))
    return sorted(ports)

def grab_banner(ip, port):
    try:
        with socket.socket() as s:
            s.settimeout(2)
            s.connect((ip, port))
            s.sendall(b"HEAD / HTTP/1.1\r\n\r\n")
            return s.recv(1024).decode(errors="ignore").strip()
    except:
        return ""

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            banner = grab_banner(ip, port)
            logging.info(f"{ip}:{port} open | {service}")
            return (ip, port, service, banner)
    except Exception as e:
        logging.warning(f"{ip}:{port} error: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Advanced Multi-Target Port Scanner (Cross-Platform)")
    parser.add_argument("-f", "--file", help="File with list of targets (one per line)", required=True)
    parser.add_argument("-p", "--ports", help="Comma-separated ports or ranges (e.g. 22,80,1000-2000)")
    parser.add_argument("-o", "--output", help="CSV output file", required=True)
    parser.add_argument("-t", "--threads", help="Number of threads (default: 100)", type=int, default=100)
    parser.add_argument("--filter", help="Only include banners containing this keyword")
    parser.add_argument("--fast", help="Scan only top 1000 common ports", action="store_true")

    args = parser.parse_args()
    log_file = setup_logger()

    # --------------------------------
    # Load targets or create the file
    # --------------------------------
    if not os.path.isfile(args.file):
        print(Fore.RED + f"[-] File not found: {args.file}")
        if os.path.basename(args.file) == "targets.txt":
            try:
                with open(args.file, "w") as f:
                    f.write("# Add one IP or hostname per line\n")
                print(Fore.YELLOW + f"[+] Created a new empty file: {args.file}")
                print(Fore.CYAN + f"[!] Please edit the file and add your targets before re-running.")
            except Exception as e:
                print(Fore.RED + f"[-] Failed to create {args.file}: {e}")
        return
    else:
        try:
            with open(args.file, "r") as f:
                targets = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(Fore.RED + f"[-] Could not read file {args.file}: {e}")
            return

    if not targets:
        print(Fore.RED + "[-] Target file is empty. Please add one target per line.")
        return

    if args.fast:
        ports = TOP_PORTS
        print(Fore.CYAN + f"[!] Fast scan enabled. Scanning top {len(ports)} ports.")
    elif args.ports:
        ports = parse_ports(args.ports)
    else:
        ports = list(range(1, 65536))
        print(Fore.YELLOW + f"[!] No ports specified. Scanning ALL 65535 TCP ports. This may take a while...")

    print(Fore.CYAN + f"[+] Scanning {len(targets)} targets on {len(ports)} ports each.\n")
    results = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_scan = {}
        for target in targets:
            try:
                ip = socket.gethostbyname(target)
            except socket.gaierror:
                print(Fore.RED + f"[-] Cannot resolve {target}. Skipping.")
                continue
            for port in ports:
                future = executor.submit(scan_port, ip, port)
                future_to_scan[future] = target

        for future in tqdm(as_completed(future_to_scan), total=len(future_to_scan), desc="Scanning", ncols=80):
            result = future.result()
            if result:
                ip, port, service, banner = result
                if args.filter and args.filter.lower() not in banner.lower():
                    continue
                print(Fore.GREEN + f"[+] {ip}:{port} open | {service} | {banner[:60]}")
                results.append(result)

    try:
        output_path = os.path.abspath(args.output)
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["IP", "Port", "Service", "Banner"])
            for row in results:
                writer.writerow(row)
        print(f"\n{Fore.YELLOW}[+] Results saved to: {output_path}")
        logging.info(f"Results saved to: {output_path}")
    except Exception as e:
        print(Fore.RED + f"[-] Failed to write CSV: {e}")
        logging.error(f"Failed to write CSV: {e}")

    print(Fore.CYAN + f"\n[+] Scan complete. {len(results)} open ports found across {len(targets)} hosts.")
    logging.info(f"Scan complete. {len(results)} results.")
    logging.info(f"Log saved to {log_file}")

if __name__ == "__main__":
    main()
