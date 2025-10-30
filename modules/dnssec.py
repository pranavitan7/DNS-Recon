import subprocess
import shlex
from rich.console import Console
from rich.table import Table
from colorama import Fore, init
import re

init(autoreset=True) 
console = Console()

def banner():
    console.print(Fore.GREEN + """
    =========================================
            DNSSEC Validation Tool
    =========================================
    """)

def run_dig_query(domain, record_type):
    """Executes the dig command and returns the output"""
    try:
        command = f"dig +dnssec {domain} {record_type}"
        result = subprocess.run(shlex.split(command), capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return None

def parse_dnssec_flags(dig_output):
    """Extracts DNSSEC flags from dig output"""
    flags = {
        "Recursion Desired (RD)": "❌",
        "Recursion Available (RA)": "❌",
        "TrunCation (TC)": "❌",
        "Authentic Data (AD)": "❌",
        "Checking Disabled (CD)": "❌"
    }

    # Extract the "flags:" line from dig output
    match = re.search(r"flags: (.+?);", dig_output)
    if match:
        flag_str = match.group(1)
        if "rd" in flag_str:
            flags["Recursion Desired (RD)"] = "✅"
        if "ra" in flag_str:
            flags["Recursion Available (RA)"] = "✅"
        if "tc" in flag_str:
            flags["TrunCation (TC)"] = "✅"
        if "ad" in flag_str:
            flags["Authentic Data (AD)"] = "✅"
        if "cd" in flag_str:
            flags["Checking Disabled (CD)"] = "✅"

    return flags

def check_dnssec(domain):
    """Checks DNSSEC records and their status"""
    records = {
        "DNSKEY": run_dig_query(domain, "DNSKEY"),
        "DS": run_dig_query(domain, "DS"),
        "RRSIG": run_dig_query(domain, "RRSIG")
    }

    # Parse flags from the DNSKEY query output
    dnssec_flags = parse_dnssec_flags(records["DNSKEY"] or "")

    return records, dnssec_flags

def display_results(domain, records, status):
    """Displays DNSSEC validation results in a structured table"""
    console.print(f"\n[bold yellow]DNSSEC Validation for:[/bold yellow] {domain}\n")

    for record_type, record_data in records.items():
        present = "✅" if record_data and "ANSWER SECTION" in record_data else "❌ No"
        table = Table(title=f"[bold green]{record_type} - Present? {present}[/bold green]")
        table.add_column("Feature", style="cyan", justify="left")
        table.add_column("Status", style="bold", justify="center")

        for feature, symbol in status.items():
            table.add_row(feature, symbol)

        console.print(table)

def main():
    banner()

    domain = input(Fore.CYAN + "\nEnter the domain to check: ").strip()

    if not domain:
        console.print(Fore.RED + "[!] Invalid input. Please enter a valid domain.")
        return

    console.print(Fore.WHITE + f"[*] Checking DNSSEC for: {domain}")

    dnssec_records, dnssec_status = check_dnssec(domain)

    display_results(domain, dnssec_records, dnssec_status)

    console.print(Fore.GREEN + "[*] DNSSEC check completed.")

if __name__ == "__main__":
    main()
