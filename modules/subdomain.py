import requests
import re
from colorama import Fore, init
from rich.console import Console
from rich.table import Table

# Initialize Colorama and Rich
init(autoreset=True)
console = Console()

# Banner
def banner():
    console.print(Fore.CYAN + """
    =============================================
                   Subdomain Finder
    =============================================
    """)

# Fetch subdomains from crt.sh
def fetch_subdomains_crtsh(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                subdomains.add(entry['name_value'])
    except requests.RequestException as e:
        console.print(Fore.RED + f"[!] crt.sh Error: {e}")
    return subdomains

# Fetch subdomains from AlienVault OTX API
def fetch_subdomains_otx(domain):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    subdomains = set()
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data.get("passive_dns", []):
                subdomains.add(entry["hostname"])
    except requests.RequestException as e:
        console.print(Fore.RED + f"[!] AlienVault OTX API Error: {e}")
    return subdomains

# Clean subdomains
def clean_subdomains(subdomains, domain):
    unique_subdomains = set()
    pattern = re.compile(rf"^[a-zA-Z0-9.-]*\.{re.escape(domain)}$")

    for sub in subdomains:
        sub = sub.strip().lower()
        if pattern.match(sub):
            unique_subdomains.add(sub)

    return sorted(unique_subdomains)

# Display results in a formatted table
def display_subdomains(subdomains, domain):
    console.print(Fore.WHITE + f"[*] Enumerating subdomains for: {domain}")

    if not subdomains:
        console.print(Fore.YELLOW + "[!] No subdomains found.")
    else:
        table = Table(title=f"Discovered Subdomains for {domain}", header_style="bold green")
        table.add_column("Subdomains", style="cyan", justify="left")
        for sub in subdomains:
            table.add_row(sub)
        console.print(table)

# Main function
def main():
    banner()
    domain = input(Fore.CYAN + "[?] Enter the target domain: ").strip()

    subdomains_crtsh = fetch_subdomains_crtsh(domain)
    subdomains_otx = fetch_subdomains_otx(domain)

    all_subdomains = subdomains_crtsh | subdomains_otx
    cleaned_subdomains = clean_subdomains(all_subdomains, domain)

    display_subdomains(cleaned_subdomains, domain)

    console.print(Fore.GREEN + f"[*] Enumeration completed: {len(cleaned_subdomains)} subdomains found.")

# Entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(Fore.RED + "\n[!] Process interrupted by user.")
