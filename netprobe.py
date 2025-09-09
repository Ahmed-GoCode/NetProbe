# -*- coding: utf-8 -*-
"""
NetProbe v2.0 - A Lightweight Network Utility
A command-line based utility for network reconnaissance and analysis.

Features:
- Port scanning with multi-threaded execution
- Hostname resolution
- Network connectivity testing

Author: Ahmad
Educational and research purposes only.
"""

import socket
import threading
import time
import os
import sys
import argparse
from queue import Queue
from colorama import Fore, Style, init

# --- Initialize colorama for colored output ---
init(autoreset=True)

# --- Core Configuration ---
queue = Queue()
open_ports = []

# --- Utility Functions ---
def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_target(target):
    """Validate target hostname/IP and prevent internal/localhost access."""
    if not target:
        return False, "No target specified."
    
    # Prevent localhost/internal IP attacks
    forbidden_targets = ['localhost', '127.0.0.1', '0.0.0.0', '::1']
    if target.lower() in forbidden_targets:
        return False, "Scanning localhost/internal IPs is not allowed for security reasons."
    
    # Check for private IP ranges
    try:
        ip = socket.inet_aton(target)
        ip_int = int.from_bytes(ip, byteorder='big')
        # 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
        private_ranges = [
            (0x0A000000, 0x0AFFFFFF),  # 10.0.0.0/8
            (0xAC100000, 0xAC1FFFFF),  # 172.16.0.0/12
            (0xC0A80000, 0xC0A8FFFF),  # 192.168.0.0/16
        ]
        for start, end in private_ranges:
            if start <= ip_int <= end:
                return False, "Scanning private IP ranges is not recommended."
    except socket.error:
        pass  # Not an IP address, might be a hostname
    
    return True, "Target is valid."

def get_target():
    """Prompt user for target hostname/IP with validation."""
    print(f"{Fore.CYAN}[INPUT]{Style.RESET_ALL} Enter Target Hostname or IP:")
    target = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()
    
    valid, message = validate_target(target)
    if not valid:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
        time.sleep(1.5)
        return None
    
    return target

def resolve_hostname(hostname):
    """Resolve hostname to IP address."""
    try:
        ip = socket.gethostbyname(hostname)
        print(f"{Fore.GREEN}[RESOLVED]{Style.RESET_ALL} {hostname} -> {ip}")
        time.sleep(1)
        return ip
    except socket.gaierror:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Could not resolve hostname '{hostname}'.")
        time.sleep(1.5)
        return None

def get_integer_input(prompt, default, min_val=1, max_val=65535):
    """Get an integer input from the user with validation."""
    user_input = input(f"{Fore.CYAN}[INPUT]{Style.RESET_ALL} {prompt} (Default: {default}): ").strip()
    if user_input == "":
        return default
    try:
        value = int(user_input)
        if min_val <= value <= max_val:
            return value
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Value must be between {min_val} and {max_val}. Using default: {default}")
            time.sleep(1)
            return default
    except ValueError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid input. Using default: {default}")
        time.sleep(1)
        return default

# --- Port Scanning Functions ---
def scan_port(ip, port):
    """Check if a single port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout for connection attempt
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def fill_port_queue(port_list):
    """Add ports to the scanning queue."""
    for port in port_list:
        queue.put(port)

def worker_thread(ip):
    """Worker thread for scanning ports."""
    global open_ports
    while not queue.empty():
        port = queue.get()
        if scan_port(ip, port):
            print(f"{Fore.GREEN}[OPEN]{Style.RESET_ALL} Port {port}")
            open_ports.append(port)
        queue.task_done()  # Mark task as done

def run_port_scan(target_ip, scan_range, num_threads):
    """Execute the port scanning process."""
    global open_ports
    open_ports = []  # Reset list for new scan
    print(f"{Fore.YELLOW}[SCANNING]{Style.RESET_ALL} {target_ip} (Ports 1-{scan_range}) with {num_threads} threads...")
    
    port_list = range(1, scan_range + 1)
    fill_port_queue(port_list)
    
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=lambda: worker_thread(target_ip))
        t.daemon = True
        threads.append(t)
        t.start()
    
    # Wait for all threads to finish
    for t in threads:
        t.join()
    
    print(f"{Fore.GREEN}[DONE]{Style.RESET_ALL} Scan finished. Open ports found: {len(open_ports)}")
    if open_ports:
        print(f"{Fore.CYAN}[RESULTS]{Style.RESET_ALL} Open Ports: {', '.join(map(str, open_ports))}")
    return open_ports

def ping_host(hostname):
    """Simple connectivity test to a host."""
    try:
        # Try to connect to port 80 (HTTP) for basic connectivity
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((hostname, 80))
        sock.close()
        
        if result == 0:
            print(f"{Fore.GREEN}[PING]{Style.RESET_ALL} {hostname} is reachable (port 80 open)")
            return True
        else:
            # Try port 443 (HTTPS)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((hostname, 443))
            sock.close()
            
            if result == 0:
                print(f"{Fore.GREEN}[PING]{Style.RESET_ALL} {hostname} is reachable (port 443 open)")
                return True
            else:
                print(f"{Fore.YELLOW}[PING]{Style.RESET_ALL} {hostname} may be unreachable or blocking connections")
                return False
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Ping failed: {e}")
        return False

# --- Main Menu and Execution ---
def show_menu():
    """Display the main menu options."""
    clear_screen()
    print(f"{Fore.GREEN}--- NetProbe v2.0 - Network Utility ---{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Port Scanner")
    print(f"{Fore.BLUE}[2]{Style.RESET_ALL} Hostname Resolution")
    print(f"{Fore.MAGENTA}[3]{Style.RESET_ALL} Connectivity Test")
    print(f"{Fore.YELLOW}[4]{Style.RESET_ALL} Exit")
    print("-" * 40)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='NetProbe v2.0 - A lightweight network utility tool',
        epilog='Example: python netprobe.py --scan google.com --ports 1000 --threads 50'
    )
    
    parser.add_argument('--scan', '-s', type=str, help='Target hostname or IP to scan')
    parser.add_argument('--ports', '-p', type=int, default=1000, help='Port range to scan (1 to N, default: 1000)')
    parser.add_argument('--threads', '-t', type=int, default=50, help='Number of threads (default: 50)')
    parser.add_argument('--resolve', '-r', type=str, help='Resolve hostname to IP address')
    parser.add_argument('--ping', type=str, help='Test connectivity to a host')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    
    return parser.parse_args()

def main():
    """Main program entry point."""
    args = parse_arguments()
    
    # Command line mode
    if args.scan:
        if not args.scan.strip():
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Empty target provided.")
            sys.exit(1)
            
        valid, message = validate_target(args.scan)
        if not valid:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
            sys.exit(1)
        
        ip = resolve_hostname(args.scan)
        if ip:
            ports = max(1, min(args.ports, 65535))
            threads = max(1, min(args.threads, 200))
            run_port_scan(ip, ports, threads)
        return
    
    if args.resolve:
        ip = resolve_hostname(args.resolve)
        return
    
    if args.ping:
        valid, message = validate_target(args.ping)
        if not valid:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
            sys.exit(1)
        
        ip = resolve_hostname(args.ping)
        if ip:
            ping_host(ip)
        return
    
    # Interactive mode (default)
    try:
        while True:
            show_menu()
            option = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()

            if option == "1":
                clear_screen()
                target = get_target()
                if target:
                    ip = resolve_hostname(target)
                    if ip:
                        scan_range = get_integer_input("Port Scan Range (e.g., 1000 for ports 1-1000)", 1000, 1, 65535)
                        threads = get_integer_input("Number of Scanner Threads", 50, 1, 200)
                        run_port_scan(ip, scan_range, threads)
                        input(f"{Fore.MAGENTA}[PAUSE]{Style.RESET_ALL} Press Enter to return to the menu...")
            
            elif option == "2":
                clear_screen()
                target = get_target()
                if target:
                    resolve_hostname(target)
                    input(f"{Fore.MAGENTA}[PAUSE]{Style.RESET_ALL} Press Enter to return to the menu...")
            
            elif option == "3":
                clear_screen()
                target = get_target()
                if target:
                    ip = resolve_hostname(target)
                    if ip:
                        ping_host(ip)
                    input(f"{Fore.MAGENTA}[PAUSE]{Style.RESET_ALL} Press Enter to return to the menu...")
            
            elif option == "4":
                clear_screen()
                print(f"{Fore.GREEN}[EXIT]{Style.RESET_ALL} Goodbye!")
                time.sleep(1)
                break
            
            else:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid option selected.")
                time.sleep(1.5)
    except EOFError:
        print(f"\n{Fore.YELLOW}[EXIT]{Style.RESET_ALL} Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[EXIT]{Style.RESET_ALL} Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[CRITICAL ERROR]{Style.RESET_ALL} {e}")
        sys.exit(1)