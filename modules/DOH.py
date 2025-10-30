import requests
from rich.console import Console
from rich.table import Table
from colorama import Fore, init, Back, Style
from time import sleep

# Initialize colorama
init(autoreset=True)
console = Console()

# Google DoH API URL 
DOH_API = "https://dns.google/resolve"

from colorama import Fore, Back, Style
from time import sleep
from rich.console import Console

console = Console()

def banner():
    console.print(Fore.GREEN + """
============================================
       DoH Checker - DNS Over HTTPS
============================================
""")
# Call the banner function to see the result
banner()

def get_user_domain():
    """ Prompt user to enter a valid domain """
    while True:
        domain = input(Fore.CYAN + "[?] Enter domain name (example.com): ").strip()
        if domain and "." in domain:
            return domain
        console.print(Fore.RED + "[!] Invalid input. Please enter a valid domain.")

def check_dns_over_https(domain):
    try:
        api_url = f"https://dns.google/resolve?name={domain}&type=A"
        response = requests.get(api_url, timeout=10)  # Fixed timeout to prevent hanging

        if response.status_code == 200:
            data = response.json()

            # Check if the response contains an error (NXDOMAIN or SERVFAIL)
            if "Status" in data and data["Status"] != 0:
                return "Not Supported"

            return "Supported"
        return "Not Supported"

    except requests.RequestException as e:
        console.print(Fore.RED + f"[!] Error checking DNS over HTTPS: {e}")
        return "Not Supported"

def display_results(domain, status):
    """ Display results in a structured table """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Domain", style="cyan", justify="left")
    table.add_column("DoH Support", style="green", justify="left")

    table.add_row(domain, status)
    console.print(table)

def main():
    banner()
    domain = get_user_domain()
    console.print(Fore.WHITE + f"[*] Checking DNS over HTTPS support for: {domain}")
    doh_status = check_dns_over_https(domain)

    if doh_status:
        display_results(domain, doh_status)
    else:
        console.print(Fore.RED + "[!] Unable to determine DoH support.")

    console.print(Fore.CYAN + "[*] DNS Over HTTPS check completed.")

if __name__ == "__main__":
    main()
