#!/usr/bin/env python3
"""
7KPM Wi-Fi Connection Tool using nmcli + password list support
"""

import subprocess
import sys
import time
import os
from getpass import getpass
from typing import List, Dict

if os.geteuid() != 0:
    print("\033[91m❌ This script must be run as root!\033[0m")
    print("👉 Try: sudo python3 password_guesser.py")
    sys.exit(1)

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_big_title():
    print(f"\n{CYAN}{BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║     ███████╗ ██╗  ██╗ ██████╗ ███╗   ███╗                  ║")
    print("║         ██╔╝ ██║ ██╔╝ ██╔══██╗████╗ ████║                  ║")
    print("║        ██╔╝  █████╔╝  ██████╔╝██╔████╔██║                  ║")
    print("║       ██╔╝   ██╔═██╗  ██╔═══╝ ██║╚██╔╝██║                  ║")
    print("║      ██     ╗██║  ██╗ ██║     ██║ ╚═╝ ██║                  ║")
    print("║      ╚══════╝╚═╝  ╚═╝ ╚═╝     ╚═╝     ╚═╝                  ║")
    print("║                                                            ║")
    print("║               Wi-Fi Connector • 2026 edition               ║")
    print("║                         7KPM                               ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

def run(cmd: list, timeout: int = 60) -> str:
    try:
        result = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"{RED}Command timed out after {timeout}s{RESET}")
        return ""
    except Exception as e:
        print(f"{RED}Command error: {e}{RESET}")
        return ""

def get_wifi_interface() -> str:
    output = run(["nmcli", "-t", "-f", "DEVICE,TYPE,STATE", "device"])
    for line in output.splitlines():
        parts = line.split(":", 2)
        if len(parts) == 3 and parts[1] == "wifi":
            return parts[0]
    print(f"{RED}No Wi-Fi interface found. Run 'nmcli radio wifi on'{RESET}")
    sys.exit(1)

def scan_wifi(interface: str) -> List[Dict]:
    print(f"{CYAN}Scanning...{RESET}", end="", flush=True)
    cmd = ["nmcli", "device", "wifi", "list", "ifname", interface]
    output = run(cmd, timeout=30)
    print(f"{GREEN} done{RESET}")
    networks = []
    seen = set()
    lines = output.splitlines()
    if lines and "IN-USE" in lines[0]:
        lines = lines[1:]
    for line in lines:
        line = line.rstrip()
        if not line.strip():
            continue
        tokens = line.split()
        if len(tokens) < 8:
            continue
        in_use = tokens[0] == '*'
        start = 1 if in_use else 0
        ssid = ""
        try:
            infra_idx = tokens.index("Infra")
            ssid = " ".join(tokens[start+1:infra_idx]).strip()
        except ValueError:
            ssid = " ".join(tokens[start+1:-5]).strip()
        security = tokens[-1] if tokens[-1] != "--" else "Open"
        signal = tokens[-2] if tokens[-2].isdigit() else "0"
        signal_int = int(signal)
        if not ssid or ssid in seen:
            continue
        seen.add(ssid)
        networks.append({
            "ssid": ssid,
            "in_use": in_use,
            "security": security,
            "signal": signal_int,
        })
    networks.sort(key=lambda x: (not x["in_use"], -x["signal"]))
    return networks

def print_networks(networks: List[Dict]):
    if not networks:
        print(f"{YELLOW}No networks found. Move closer or enable Wi-Fi.{RESET}")
        return
    print(f"\n{BOLD}{'═' * 60}{RESET}")
    print(f"{'#':2} {'★':1} {'SSID':<30} {'Sec':<8} {'Signal':>6}")
    print(f"{'─' * 60}")
    for i, n in enumerate(networks, 1):
        mark = f"{GREEN}★{RESET}" if n["in_use"] else " "
        print(f"{i:2d} {mark} {n['ssid']:<30} {n['security']:<8} {n['signal']:>5}%")
    print(f"{'═' * 60}\n")

def try_connect(interface: str, ssid: str, password: str = "") -> bool:
    print(f"  Trying → {password if password else '[open]'} ", end="", flush=True)
    subprocess.run(["nmcli", "connection", "delete", ssid],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cmd = ["nmcli", "device", "wifi", "connect", ssid, "ifname", interface]
    if password:
        cmd += ["password", password]
    try:
        result = subprocess.run(cmd, text=True, capture_output=True, timeout=60)
        output = (result.stdout + result.stderr).lower()
        if result.returncode == 0 or "successfully" in output:
            print(f"\n{GREEN}✓ SUCCESS! Connected!{RESET}")
            return True
        else:
            print(f" {RED}× Failed{RESET}")
            return False
    except subprocess.TimeoutExpired:
        print(f" {RED}Timed out{RESET}")
        return False
    except Exception:
        print(f" {RED}Error{RESET}")
        return False

def try_passwords_from_file(interface: str, ssid: str, filepath: str) -> bool:
    if not os.path.isfile(filepath):
        print(f"{RED}File not found: {filepath}{RESET}")
        return False
    with open(filepath, encoding="utf-8", errors="ignore") as f:
        passwords = list(set(line.strip() for line in f if line.strip()))
    if not passwords:
        print(f"{YELLOW}File is empty{RESET}")
        return False
    print(f"\n{YELLOW}Trying {len(passwords)} passwords automatically...{RESET}\n")
    for i, pwd in enumerate(passwords, 1):
        print(f"[{i}/{len(passwords)}] ", end="", flush=True)
        if try_connect(interface, ssid, pwd):
            return True
        time.sleep(1)
    print(f"\n{RED}No password succeeded.{RESET}")
    return False

def main():
    print_big_title()
    try:
        interface = get_wifi_interface()
        print(f"Interface → {CYAN}{interface}{RESET}\n")
        while True:
            networks = scan_wifi(interface)
            print_networks(networks)
            if not networks:
                input(f"{YELLOW}Press Enter to rescan...{RESET}")
                continue
            choice = input(f"Select network (1-{len(networks)}) or q to quit: ").strip().lower()
            if choice in ('q', 'quit', 'exit'):
                print(f"\n{GREEN}Goodbye!{RESET}")
                return
            if not choice.isdigit():
                print(f"{YELLOW}Enter a number or q{RESET}")
                time.sleep(1.2)
                continue
            idx = int(choice) - 1
            if not (0 <= idx < len(networks)):
                print(f"{YELLOW}Invalid choice{RESET}")
                time.sleep(1.2)
                continue
            selected = networks[idx]
            ssid = selected["ssid"]
            print(f"\nSelected → {BOLD}{ssid}{RESET} ({selected['security']}, {selected['signal']}%)")
            if selected["security"] == "Open":
                print(f"{GREEN}No password needed! Connecting...{RESET}")
                try_connect(interface, ssid, "")
                input("\nPress Enter to exit...")
                return
            print("\nPassword options:")
            print(" 1) Enter password manually")
            print(" 2) Try passwords from a file (.txt)")
            print(" 3) Skip")
            opt = input("Choose [1/2/3]: ").strip()
            success = False
            if opt == "1":
                pwd = getpass(f"Password for '{ssid}': ")
                if pwd.strip():
                    success = try_connect(interface, ssid, pwd)
            elif opt == "2":
                path = input("Path to password file (txt): ").strip()
                if path:
                    success = try_passwords_from_file(interface, ssid, path)
            elif opt == "3":
                print(f"{YELLOW}Skipped.{RESET}")
                continue
            else:
                print(f"{YELLOW}Invalid choice → back to menu{RESET}")
                time.sleep(1.2)
                continue
            if success:
                print(f"\n{GREEN}Connection successful! You can close this window.{RESET}")
                input("\nPress Enter to exit...")
                return
            else:
                print(f"\n{YELLOW}Failed. Try again?{RESET}")
                input("Press Enter to continue...")
    except KeyboardInterrupt:
        print(f"\n\n{CYAN}Exited by user. Bye!{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()

