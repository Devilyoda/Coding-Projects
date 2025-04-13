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

def run_tool(tool, args="", background=False):
    cmd = f"{TOOLS[tool]} {args}"
    console.print(f"\n[bold green][+] Running:[/bold green] {cmd}\n")
    if background:
        subprocess.Popen(cmd, shell=True)
    else:
        subprocess.call(cmd, shell=True)

def is_windows():
    return platform.system().lower() == "windows"

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

def netwatch_menu():
    while True:
        print("""
======= NetWatch Setup =======
1. Quick scan (Local LAN, baseline off)
2. Recommended scan (targets.txt, baseline ON)
3. Custom options
0. Return to NetControl
        """)

        quick_choice = input("Select option [0-3]: ").strip()

        if quick_choice == "0":
            return

        if quick_choice == "1":
            target_file = "temp_net_targets.txt"
            with open(target_file, "w") as f:
                f.write("192.168.1.1\n192.168.1.254\n")
            args = f"-f {target_file} -o netwatch_quick.csv --interval 30 -t 50"
            run_tool("netwatch", args)
            return

        elif quick_choice == "2":
            target_file = "targets.txt"
            args = f"-f {target_file} -o netwatch_log.csv --interval 60 -t 50 --baseline"
            run_tool("netwatch", args)
            return

        elif quick_choice == "3":
            print("""
NetWatch Custom Presets:
1. Common LAN targets (192.168.1.1, 192.168.1.254)
2. File: targets.txt (default)
3. Custom input (CIDR or hostnames)
            """)

            target_choice = input("Choose target set [1-3]: ").strip()
            if target_choice == "1":
                target_file = "temp_net_targets.txt"
                with open(target_file, "w") as f:
                    f.write("192.168.1.1\n192.168.1.254\n")
            elif target_choice == "2":
                target_file = "targets.txt"
            elif target_choice == "3":
                user_input = input("Enter subnet or hostnames (comma separated): ").strip()
                targets = resolve_targets_input(user_input)
                target_file = "temp_custom_targets.txt"
                with open(target_file, "w") as f:
                    for ip in targets:
                        f.write(ip + "\n")
            else:
                print("Invalid option. Defaulting to targets.txt")
                target_file = "targets.txt"

            baseline = input("Enable baseline tracking? [Y/n]: ").strip().lower()
            use_baseline = "--baseline" if baseline in ["y", "yes", ""] else ""

            interval = input("Enter scan interval (seconds) [default 60]: ").strip() or "60"
            threads = input("Enter thread count [default 50]: ").strip() or "50"
            output = input("Enter CSV output file name [default: netwatch_log.csv]: ").strip() or "netwatch_log.csv"

            if is_windows():
                print("[!] Windows detected. Ensure 'ping' is available and compatible.")

            args = f"-f {target_file} -o {output} --interval {interval} -t {threads} {use_baseline}"
            run_tool("netwatch", args)
            return

        else:
            print("[!] Invalid option. Please select 0-3.")
