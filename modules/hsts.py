import requests
from rich.console import Console
from rich.table import Table
from colorama import Fore, init

init(autoreset=True)
console = Console()

def banner():
    console.print(Fore.GREEN + """
    ==========================================
         HSTS Check Tool - Secure or Not?
    ==========================================
    """)

def check_hsts(domain):
    url = f"https://{domain}"
    try:
        response = requests.get(url, timeout=10)
        hsts_header = response.headers.get("Strict-Transport-Security")

        if hsts_header:
            hsts_data = parse_hsts_header(hsts_header)
            hsts_data["enabled"] = "✅ Yes"
            return hsts_data
        else:
            return {"enabled": "❌ No", "max-age": "N/A", "includeSubDomains": "N/A", "preload": "N/A"}
    except requests.exceptions.RequestException as e:
        console.print(Fore.RED + f"[!] Error: {e}")
        return None

def parse_hsts_header(header):
    parts = header.lower().split(";")
    hsts_info = {
        "max-age": "N/A",
        "includeSubDomains": "false",
        "preload": "false"
    }
    for part in parts:
        part = part.strip()
        if part.startswith("max-age="):
            hsts_info["max-age"] = part.split("=")[1]
        elif part == "includesubdomains":
            hsts_info["includeSubDomains"] = "true"
        elif part == "preload":
            hsts_info["preload"] = "true"
    return hsts_info

def display_hsts_status(domain, hsts_data):
    table = Table(show_header=False)
    table.add_column("", style="bold cyan")
    table.add_column("", style="bold white")

    table.add_row("HSTS Enabled?", hsts_data["enabled"])
    table.add_row("max-age", hsts_data["max-age"])
    table.add_row("includeSubDomains", hsts_data["includeSubDomains"])
    table.add_row("preload", hsts_data["preload"])

    console.print("\n[bold green]HSTS Check[/bold green]")
    console.print(table)

    if hsts_data["preload"] == "true":
        console.print(Fore.GREEN + "Site is compatible with the HSTS preload list!")
    else:
        console.print(Fore.YELLOW + "Site is NOT in the HSTS preload list.")

def main():
    banner()
    domain = console.input(Fore.YELLOW + "[?] Enter the domain (without http/https): ").strip()

    if not domain:
        console.print(Fore.RED + "[!] Invalid input. Please enter a valid domain.")
        return

    console.print(Fore.WHITE + f"[*] Checking HSTS for: {domain}")
    hsts_data = check_hsts(domain)

    if hsts_data:
        display_hsts_status(domain, hsts_data)
    else:
        console.print(Fore.RED + "[!] Could not retrieve HSTS information.")

    console.print(Fore.CYAN + "[*] HSTS check completed.")

if __name__ == "__main__":
    main()
