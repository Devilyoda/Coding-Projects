#!/usr/bin/env python3
"""
LogWatch - Firewall & IDS Log Analyzer (Cross-Platform)

Analyzes system, firewall, or IDS logs (e.g., UFW, iptables, Suricata, Snort).
Supports static log review or live tailing mode.

Features:
- Filter logs by keyword (e.g., DROP, scan, alert)
- Regex support for advanced pattern matching
- Highlight lines by IP, port, or string
- Real-time tailing (`--tail`)
- Optional CSV output of filtered matches
- Optional TUI mode using rich (`--tui`)
- Color-coded rows by match type
- Live match counter in dashboard
- Live keyword histogram chart (TUI)
- Works on Linux, macOS, Windows (if logs are exported to .txt/.log)

USAGE EXAMPLES:
    logwatch -f /var/log/syslog --filter DROP
    logwatch -f firewall.log --filter alert,scan --include-ips 192.168.1.1
    logwatch -f logs/ufw.log --tail --output matches.csv
    logwatch -f /var/log/syslog --filter DROP --tail --tui

Arguments:
    -f, --file            Log file path
    --filter              Comma-separated keywords to match
    --regex               Regex pattern (overrides keyword match if used)
    --include-ips         Comma-separated IPs to highlight
    --tail                Follow the log file like `tail -f`
    --output              Save matched lines to CSV (optional)
    --tui                 Display output in a terminal UI (requires rich)

Windows Notes:
- This script does not access Windows Event Viewer directly.
- To use with Windows logs:
    1. Export logs from Event Viewer as .txt or .log
    2. Pass the exported file to logwatch

Real World Use Cases:
- Watch for blocked traffic (UFW):
      logwatch -f /var/log/ufw.log --filter DROP --tail
- Monitor scan alerts from Suricata:
      logwatch -f /var/log/suricata/fast.log --filter scan,alert --tail
- Parse exported logs from Windows:
      logwatch -f exported_eventlog.txt --filter fail,denied
- Watch internal IP for suspicious hits:
      logwatch -f /var/log/syslog --include-ips 192.168.1.10

Dependencies:
    pip install colorama
    pip install rich  # Required if using --tui
"""

# This version includes keyboard support to export matched log table from TUI.
# Press "s" while TUI is running to save current visible entries to a timestamped CSV.

import argparse
import os
import time
import csv
import re
from collections import Counter
from colorama import Fore, init
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.bar import Bar
from datetime import datetime
import threading
import sys
import select

init(autoreset=True)
console = Console()

def parse_csv_string(value):
    return [v.strip() for v in value.split(",") if v.strip()]

def line_matches(line, keywords, ips, regex):
    if regex:
        if re.search(regex, line):
            return True
    if keywords:
        for kw in keywords:
            if kw.lower() in line.lower():
                return True
    if ips:
        for ip in ips:
            if ip in line:
                return True
    return False

def get_row_style(line):
    if "DROP" in line:
        return "bold red"
    elif "ACCEPT" in line:
        return "bold green"
    elif "REJECT" in line:
        return "bold yellow"
    elif "alert" in line.lower():
        return "bold magenta"
    return "white"

def save_table_to_csv(rows):
    filename = f"logwatch_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    try:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Matched Line"])
            for row in rows:
                writer.writerow(row)
        console.print(f"[bold green][+] Saved current view to:[/] {filename}")
    except Exception as e:
        console.print(f"[bold red][-] Failed to save CSV: {e}")

def build_histogram(keyword_counter):
    top_items = keyword_counter.most_common(5)
    chart = Table.grid()
    chart.add_column(justify="left")
    chart.add_column(justify="right")
    for label, count in top_items:
        chart.add_row(f"[bold]{label}[/]", Bar(size=count, begin=0, end=max(1, count), width=20))
    return Panel(chart, title="Top Matches", border_style="cyan")

def tail_file_tui(file_path, keywords, ips, regex):
    match_count = 0
    keyword_counter = Counter()
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=3),
        Layout(name="footer", size=8)
    )

    table = Table(expand=True)
    table.add_column("Time", style="cyan", width=10)
    table.add_column("Matched Line", style="white", overflow="fold")

    log_rows = []

    def input_listener():
        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1)
                if key.lower() == "s":
                    save_table_to_csv(log_rows)

    threading.Thread(target=input_listener, daemon=True).start()

    try:
        with open(file_path, "r") as f, Live(layout, refresh_per_second=4, screen=False) as live:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                if line_matches(line, keywords, ips, regex):
                    match_count += 1
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    style = get_row_style(line)
                    text = Text(line.strip(), style=style)
                    table.add_row(timestamp, text)
                    log_rows.append([timestamp, line.strip()])
                    for kw in keywords:
                        if kw.lower() in line.lower():
                            keyword_counter[kw] += 1
                    if len(table.rows) > 20:
                        table.rows.pop(0)

                    layout["header"].update(Align.center(
                        Panel(f"[bold green]Log File:[/] {file_path}    [bold yellow]Matches:[/] {match_count}    [bold blue](press 's' to save)[/]"), vertical="middle"
                    ))
                    layout["body"].update(table)
                    layout["footer"].update(build_histogram(keyword_counter))
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Log tailing stopped by user.")

def tail_file(file_path, keywords, ips, regex, csv_out):
    print(Fore.CYAN + f"[+] Tailing {file_path}... (Press Ctrl+C to stop)")
    try:
        with open(file_path, "r") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                if line_matches(line, keywords, ips, regex):
                    print(Fore.GREEN + line.strip())
                    if csv_out:
                        csv_out.writerow([line.strip()])
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Log tailing stopped by user.")

def scan_file(file_path, keywords, ips, regex, csv_out):
    print(Fore.CYAN + f"[+] Scanning {file_path} for matches...")
    try:
        with open(file_path, "r") as f:
            for line in f:
                if line_matches(line, keywords, ips, regex):
                    print(Fore.GREEN + line.strip())
                    if csv_out:
                        csv_out.writerow([line.strip()])
    except Exception as e:
        print(Fore.RED + f"[-] Error reading file: {e}")

def main():
    parser = argparse.ArgumentParser(description="LogWatch - Firewall & IDS Log Analyzer")
    parser.add_argument("-f", "--file", help="Log file path", required=True)
    parser.add_argument("--filter", help="Comma-separated keywords")
    parser.add_argument("--include-ips", help="Comma-separated IPs to highlight")
    parser.add_argument("--regex", help="Regex pattern to match lines")
    parser.add_argument("--tail", help="Follow log file in real time", action="store_true")
    parser.add_argument("--output", help="Output CSV file (optional)")
    parser.add_argument("--tui", help="Display output in a terminal UI (requires rich)", action="store_true")

    args = parser.parse_args()
    if not os.path.isfile(args.file):
        print(Fore.RED + f"[-] File not found: {args.file}")
        return

    keywords = parse_csv_string(args.filter) if args.filter else []
    ips = parse_csv_string(args.include_ips) if args.include_ips else []
    regex = args.regex if args.regex else None

    csv_writer = None
    if args.output:
        try:
            out_file = open(args.output, "w", newline="")
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(["Matched Line"])
        except Exception as e:
            print(Fore.RED + f"[-] Failed to open CSV: {e}")
            return

    if args.tail:
        if args.tui:
            tail_file_tui(args.file, keywords, ips, regex)
        else:
            tail_file(args.file, keywords, ips, regex, csv_writer)
    else:
        scan_file(args.file, keywords, ips, regex, csv_writer)

    if csv_writer:
        out_file.close()
        print(Fore.YELLOW + f"[+] Output saved to {args.output}")

if __name__ == "__main__":
    main()
