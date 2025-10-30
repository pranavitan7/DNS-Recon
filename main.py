import os
import sys
import time
import subprocess
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)

def banner():
    os.system("clear")
    print(Fore.CYAN + Style.BRIGHT + """
┌────────────────────────────────────────────────────────────┐
│                    DNS RECOGNITION TOOL                    │
├────────────────────────────────────────────────────────────┤
                 Developed with 💻 by Pranavi               
└────────────────────────────────────────────────────────────┘
""")

    print(Fore.YELLOW + """
+-------------------------------------------------------------+
| Welcome to the DNS Recognition Tool!                        |
| This tool is designed to help you explore and analyze the   |
| Domain Name System (DNS) of any website in a simple and     |
| informative way by fetching essential information such as   |
| DNS records (A, MX, NS, TXT), checking for DNSSEC (security |
| extensions that protect DNS data), looking up domain crawl  |
| rules (via robots.txt), crawling the domain to identify     |
| internal links and structure, verifying if the domain uses  |
| HSTS (a security feature enforcing HTTPS), and checking if  |
| DNS queries are made over HTTPS (DoH) for privacy. This     |
| tool simplifies DNS data and security insights, making it   |
| a valuable resource for understanding website setups,       |
| security configurations, and privacy measures.              |
+-------------------------------------------------------------+
""")

def run_module(script_name):
    subprocess.run(["python", f"modules/{script_name}"])
    input(Fore.YELLOW + "\nPress Enter to return to the menu..." + Style.RESET_ALL)

def main_menu():
    menu_options = [
        ("[1]", "🔍 DNS Record Lookup"),
        ("[2]", "🛡️ DNSSEC Check"),
        ("[3]", "📜 Domain Crawl Rules Lookup"),
        ("[4]", "🕷️ Domain Crawler"),
        ("[5]", "🔒 HSTS Check"),
        ("[6]", "🌐 DOH (DNS over HTTPS)"), 
        ("[7]", "🌐 SubDomain Enumeration"),
        ("[0]", "❌ Exit")
    ]

    while True:
        banner()
        print(Fore.GREEN + Style.BRIGHT + "Select an option below:" + Style.RESET_ALL)
        print(Fore.CYAN + tabulate(menu_options, headers=["Code", "Option"], tablefmt="fancy_grid"))

        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()

        if choice == "1":
            run_module("dnsrecord.py")
        elif choice == "2":
            run_module("dnssec.py")
        elif choice == "3":
            run_module("crawl.py")
        elif choice == "4":
            run_module("crawler.py")
        elif choice == "5":
            run_module("hsts.py")
        elif choice == "6":
            run_module("DOH.py")
             elif choice == "7":
            run_module("subdomain.py")
        elif choice == "0":
            print("\n" + Fore.RED + "Exiting..." + Style.RESET_ALL)
            time.sleep(1)
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid choice! Please enter a valid option." + Style.RESET_ALL)
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
