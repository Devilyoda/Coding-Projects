#!/usr/bin/env python3
"""
NetControl - Master Controller for Network Scripts

Launch and manage all custom network/security tools from one interface.

Tools supported:
- pingsweep
- portscan
- netwatch
- servwatch
- logwatch

Usage Examples:
    netcontrol                # Interactive menu
    netcontrol --tool pingsweep --args "192.168.1.0/24 -o live_hosts.csv"
    netcontrol --run-all     # Run all tools sequentially

Requirements:
    All scripts must be globally accessible (e.g., in /usr/local/bin)
"""

import argparse
import subprocess
import sys
import textwrap
import os
import platform
import socket
import ipaddress
import time
from rich import print
from rich.console import Console

console = Console()
VERSION = "1.1"

TOOLS = {
    "pingsweep": "pingsweep",
    "portscan": "portscan",
    "netwatch": "netwatch",
    "servwatch": "servwatch",
    "logwatch": "logwatch",
}

CHANGELOG = """
Changelog:
- v1.1: Enhancements
  • Auto show banner on every run
  • Improved help formatting
- v1.0: Initial stable release
  • All 5 tools supported
  • Interactive menus with presets
  • Custom CLI argument support
  • Global launcher script ready
"""

def show_banner():
    console.print("""
╔══════════════════════════════════════════════════════╗
║     [bold green]NetControl v{} Loaded[/bold green]                         ║
╚═════════════════════════════════════════════════════╝
    """.format(VERSION))

def show_help():
    print(textwrap.dedent("""
    Usage:
        netcontrol                     # Launch interactive menu
        netcontrol --tool TOOL --args "ARGS"
        netcontrol --run-all

    Options:
        --tool        Run a specific tool (e.g. portscan)
        --args        Arguments to pass to the tool
        --run-all     Run all tools in sequence
        --version     Show version info
        --changelog   Show recent updates
    """))

def show_changelog():
    print(CHANGELOG)

def run_tool(tool, args="", background=False, timeout=None):
    cmd = f"{TOOLS[tool]} {args}"
    console.print(f"\n[bold green][+] Running:[/bold green] {cmd}\n")
    if background:
        subprocess.Popen(cmd, shell=True)
    else:
        try:
            if timeout:
                subprocess.run(cmd, shell=True, timeout=timeout)
            else:
                subprocess.call(cmd, shell=True)
        except subprocess.TimeoutExpired:
            console.print(f"[bold red]Tool '{tool}' timed out after {timeout} seconds[/bold red]")

def resolve_targets_input(input_str):
    targets = []
    for entry in input_str.split(","):
        entry = entry.strip()
        if not entry:
            continue
        try:
            if "/" in entry:
                network = ipaddress.ip_network(entry, strict=False)
                targets.extend(str(ip) for ip in network.hosts())
            else:
                ip = socket.gethostbyname(entry)
                targets.append(ip)
        except Exception as e:
            console.print(f"[yellow][-] Skipping invalid input:[/yellow] {entry} ({e})")
    return targets
def run_all_with_custom_targets():
    subnet = input("Enter subnet/hosts for pingsweep/portscan/netwatch (default 192.168.1.0/24): ").strip() or "192.168.1.0/24"
    targets = []
    if "/" in subnet:
        network = ipaddress.ip_network(subnet, strict=False)
        targets = [str(ip) for ip in network.hosts()]
    else:
        targets = [subnet]

    temp_file = "temp_runall_targets.txt"
    with open(temp_file, "w") as f:
        for ip in targets:
            f.write(ip + "\n")

    run_tool("pingsweep", f"{subnet}")
    run_tool("portscan", f"-f {temp_file} -o portscan.csv")
    run_tool("netwatch", f"-f {temp_file} -o netwatch.csv")

    service_duration = input("Enter Service Watch runtime in seconds (blank for infinite): ").strip()
    log_duration = input("Enter Log Watch runtime in seconds (blank for infinite): ").strip()

    run_tool("servwatch", "-f services.txt -o service_log.csv", timeout=int(service_duration) if service_duration else None)
    run_tool("logwatch", "-f /var/log/syslog --filter DROP", timeout=int(log_duration) if log_duration else None)

def pingsweep_menu():
    print("""
======= Ping Sweep Setup =======
1. Quick: 192.168.1.0/24
2. Common subnet: 10.0.0.0/24
3. Common subnet: 172.16.0.0/24
4. Custom subnet or hostnames
0. Return to NetControl
    """)
    choice = input("Select an option: ").strip()

    if choice == "0":
        return
    elif choice == "1":
        subnet = "192.168.1.0/24"
    elif choice == "2":
        subnet = "10.0.0.0/24"
    elif choice == "3":
        subnet = "172.16.0.0/24"
    elif choice == "4":
        subnet = input("Enter subnet or hostnames: ").strip()
    else:
        print("Invalid option.")
        return

    threads = input("Thread count (default 100): ").strip() or "100"
    output = input("Output CSV file name (optional): ").strip()

    args = f"{subnet} -t {threads}"
    if output:
        args += f" -o {output}"
    run_tool("pingsweep", args)

def portscan_menu():
    print("""
======= Port Scanner Setup =======
1. Single IP
2. Use targets.txt
3. Custom file or CIDR
0. Return to NetControl
    """)
    opt = input("Select option: ").strip()
    if opt == "0":
        return
    elif opt == "1":
        ip = input("Enter IP to scan: ").strip()
        targets = [ip]
        target_file = "temp_port_targets.txt"
        with open(target_file, "w") as f:
            for t in targets:
                f.write(t + "\n")
    elif opt == "2":
        target_file = "targets.txt"
    elif opt == "3":
        custom = input("Enter IPs, hostnames, or subnet (comma separated): ").strip()
        targets = resolve_targets_input(custom)
        target_file = "temp_custom_ports.txt"
        with open(target_file, "w") as f:
            for ip in targets:
                f.write(ip + "\n")
    else:
        print("Invalid option.")
        return

    print("""
Port Options:
1. Common ports (22,80,443)
2. Top 1000 ports (fast scan)
3. Full scan (1-65535)
4. Custom ports
    """)
    port_choice = input("Choose port scan type: ").strip()
    if port_choice == "1":
        ports = "22,80,443"
    elif port_choice == "2":
        ports = ""
    elif port_choice == "3":
        ports = "1-65535"
    elif port_choice == "4":
        ports = input("Enter ports or range (e.g., 80,443 or 1-1024): ").strip()
    else:
        ports = ""

    threads = input("Thread count (default 100): ").strip() or "100"
    output = input("Output CSV file name: ").strip()

    args = f"-f {target_file} -o {output} -t {threads}"
    if ports:
        args += f" -p {ports}"
    if port_choice == "2":
        args += " --fast"

    run_tool("portscan", args)
    print("""
Port Options:
1. Common ports (22,80,443)
2. Top 1000 ports (fast scan)
3. Full scan (1-65535)
4. Custom ports
    """)
    port_choice = input("Choose port scan type: ").strip()
    if port_choice == "1":
        ports = "22,80,443"
    elif port_choice == "2":
        ports = ""
    elif port_choice == "3":
        ports = "1-65535"
    elif port_choice == "4":
        ports = input("Enter ports or range (e.g., 80,443 or 1-1024): ").strip()
    else:
        ports = ""

    threads = input("Thread count (default 100): ").strip() or "100"
    output = input("Output CSV file name: ").strip()

    args = f"-f {target_file} -o {output} -t {threads}"
    if ports:
        args += f" -p {ports}"
    if port_choice == "2":
        args += " --fast"

    run_tool("portscan", args)

def netwatch_menu():
    print("""
======= NetWatch Setup =======
1. Quick scan (Local LAN, baseline off)
2. Recommended scan (targets.txt, baseline ON)
3. Custom options
0. Return to NetControl
    """)
    opt = input("Select option: ").strip()
    if opt == "0":
        return
    elif opt == "1":
        args = "-f temp_net_targets.txt -o netwatch_quick.csv --interval 30 -t 50"
    elif opt == "2":
        args = "-f targets.txt -o netwatch_log.csv --interval 60 -t 50 --baseline"
    elif opt == "3":
        path = input("Enter target file path: ").strip()
        interval = input("Interval in seconds (default 60): ").strip() or "60"
        output = input("Output CSV (default: netwatch_log.csv): ").strip() or "netwatch_log.csv"
        baseline = input("Enable baseline tracking? [Y/n]: ").strip().lower()
        use_baseline = "--baseline" if baseline in ["y", "yes", ""] else ""
        threads = input("Thread count (default 50): ").strip() or "50"
        args = f"-f {path} -o {output} --interval {interval} -t {threads} {use_baseline}"
    else:
        print("Invalid option.")
        return
    run_tool("netwatch", args)

def servwatch_menu():
    print("""
======= Service Watch Setup =======
1. Use default services.txt
2. Recommended: services.txt + 60s interval
3. Custom file and options
0. Return to NetControl
    """)
    opt = input("Select option: ").strip()
    if opt == "0":
        return
    elif opt == "1":
        run_tool("servwatch", "-f services.txt")
    elif opt == "2":
        run_tool("servwatch", "-f services.txt -o service_log.csv --interval 60")
    elif opt == "3":
        path = input("Enter service file path (host,port): ").strip()
        interval = input("Interval in seconds (default 60): ").strip() or "60"
        output = input("Output CSV (default: service_log.csv): ").strip() or "service_log.csv"
        args = f"-f {path} -o {output} --interval {interval}"
        run_tool("servwatch", args)
    else:
        print("Invalid option.")

def logwatch_menu():
    print("""
======= Log Watch Setup =======
1. Default syslog with DROP filter
2. Auth log with 'fail' keyword
3. Custom log path and filter
0. Return to NetControl
    """)
    choice = input("Select option: ").strip()
    if choice == "0":
        return
    elif choice == "1":
        run_tool("logwatch", "-f /var/log/syslog --filter DROP")
    elif choice == "2":
        run_tool("logwatch", "-f /var/log/auth.log --filter fail")
    elif choice == "3":
        path = input("Enter full log file path: ").strip()
        keyword = input("Enter keyword or pattern to filter: ").strip()
        output = input("Enter output CSV file name (optional): ").strip()
        args = f"-f {path} --filter {keyword}"
        if output:
            args += f" -o {output}"
        run_tool("logwatch", args)
    else:
        print("Invalid option.")

def interactive_menu():
    show_banner()
    while True:
        print("""
======= NetControl Menu =======
1. Ping Sweep
2. Port Scanner
3. Net Watch
4. Service Watch
5. Log Watch
6. Run All
0. Exit
        """)
        choice = input("Select a tool to run: ").strip()

        if choice == "1":
            pingsweep_menu()
        elif choice == "2":
            portscan_menu()
        elif choice == "3":
            netwatch_menu()
        elif choice == "4":
            servwatch_menu()
        elif choice == "5":
            logwatch_menu()
        elif choice == "6":
            run_all_with_custom_targets()
        elif choice == "0":
            print("Exiting NetControl.")
            break
        else:
            print("Invalid choice. Try again.")

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="NetControl - Master Network Tool Controller")
    parser.add_argument("--tool", help="Tool name to run (e.g. pingsweep, portscan)")
    parser.add_argument("--args", help="Arguments to pass to the tool")
    parser.add_argument("--run-all", action="store_true", help="Run all tools in order")
    parser.add_argument("--version", action="store_true", help="Show version info")
    parser.add_argument("--changelog", action="store_true", help="Show changelog")
    parser.add_argument("--help-menu", action="store_true", help="Show help info")

    args = parser.parse_args()

    if args.version:
        print(f"NetControl version {VERSION}")
    elif args.changelog:
        show_changelog()
    elif args.help_menu:
        show_help()
    elif args.run_all:
        run_all_with_custom_targets()
    elif args.tool:
        if args.tool in TOOLS:
            run_tool(args.tool, args.args or "")
        else:
            print(f"[-] Unknown tool: {args.tool}")
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
