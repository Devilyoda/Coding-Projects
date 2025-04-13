#!/usr/bin/env python3
"""
PortScan - Custom Port Scanner

Scans ports for given IPs and outputs open/closed results in a CSV file.

Usage Examples:
    portscan -f targets.txt -o results.csv -t 100 --fast
    portscan -f targets.txt -o results.csv -p 22,80,443 --timeout 3
"""

import argparse
import socket
import csv
import concurrent.futures
import ipaddress
import string
from tqdm import tqdm
from socket import getservbyport
import subprocess
import os

def clean_banner(text):
    return ''.join(c if c in string.printable else '?' for c in text).strip()

def scan_port(ip, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                try:
                    sock.sendall(b"\r\n")
                    banner = sock.recv(1024).decode(errors="ignore")
                    banner = clean_banner(banner)
                except:
                    banner = "-"
                return (ip, port, "open", get_service_name(port), banner)
            else:
                return (ip, port, "closed", get_service_name(port), "-")
    except:
        return None  # skip error ports completely

def get_service_name(port):
    try:
        return getservbyport(port)
    except:
        return "-"

def parse_ports(ports_str):
    ports = set()
    for part in ports_str.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

def load_targets(file):
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip()]

def write_csv(results, output_file):
    try:
        with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL, escapechar="\\")
            writer.writerow(["IP", "Port", "Status", "Service", "Banner"])
            for row in results:
                if row:  # Skip None values from errors
                    row = list(row)
                    row[4] = clean_banner(str(row[4]))
                    writer.writerow(row)
        print(f"[+] Results saved to: {output_file}")

        # Try to open with LibreOffice Calc
        try:
            subprocess.Popen(["libreoffice", "--calc", os.path.abspath(output_file)])
        except Exception as e:
            print(f"[!] Could not open with LibreOffice Calc: {e}")

    except Exception as e:
        print(f"[-] Failed to save CSV: {e}")

def choose_ports():
    print("""
Port Options:
1. Common ports (22,80,443)
2. Top 1000 ports (fast scan)
3. Full scan (1-65535)
4. Custom ports
    """)
    choice = input("Choose port scan type: ").strip()
    if choice == "1":
        return [22, 80, 443]
    elif choice == "2":
        return "fast"
    elif choice == "3":
        return list(range(1, 65536))
    elif choice == "4":
        custom = input("Enter ports or range (e.g., 80,443 or 1-1024): ").strip()
        return parse_ports(custom)
    else:
        print("Invalid choice, using default common ports.")
        return [22, 80, 443]

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Custom Port Scanner")
    parser.add_argument("-f", "--file", required=True, help="Input file with IPs")
    parser.add_argument("-o", "--output", required=True, help="CSV output file")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g., 80,443 or 1-1000)")
    parser.add_argument("--fast", action="store_true", help="Scan top 1000 ports")
    parser.add_argument("--timeout", type=float, default=1, help="Socket timeout")
    parser.add_argument("--clean", action="store_true", help="Remove error ports from CSV")
    args = parser.parse_args()

    top_ports = [
        21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
        1723, 3306, 3389, 5900, 8080, 8443
    ] + list(range(1, 1025))

    if args.fast:
        ports = sorted(set(top_ports))
    elif args.ports:
        ports = parse_ports(args.ports)
    else:
        ports = choose_ports()
        if ports == "fast":
            ports = sorted(set(top_ports))

    targets = load_targets(args.file)
    valid_targets = [ip for ip in targets if validate_ip(ip)]

    if not valid_targets:
        print("[-] No valid IP addresses found.")
        return

    total_tasks = len(valid_targets) * len(ports)
    print(f"[+] Scanning {len(valid_targets)} targets on {len(ports)} ports each.")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for ip in valid_targets:
            for port in ports:
                futures.append(executor.submit(scan_port, ip, port, args.timeout))

        for result in tqdm(concurrent.futures.as_completed(futures), total=total_tasks, desc="Scanning"):
            res = result.result()
            if res or not args.clean:
                results.append(res)

    write_csv(results, args.output)
    print("[+] Scan complete.")

if __name__ == "__main__":
    main()
