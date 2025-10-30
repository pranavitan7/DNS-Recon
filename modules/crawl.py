import requests
import re
from rich.console import Console
from rich.table import Table
from urllib.parse import urlparse

console = Console()

def banner():
    console.print("[bold green]\n=== Crawl Rules Checker ===\n[/bold green]")

def extract_domain(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}" if parsed_url.netloc else None

def fetch_robots_txt(url):
    domain = extract_domain(url)
    if not domain:
        console.print("[bold red][!] Invalid URL provided.[/bold red]")
        return None, None
    try:
        response = requests.get(f"{domain}/robots.txt", timeout=10)
        if response.status_code == 200:
            return domain, response.text
        return domain, None
    except requests.RequestException as e:
        console.print(f"[bold red][!] Error fetching robots.txt: {e}[/bold red]")
        return domain, None

def parse_crawl_rules(content):
    rules = []
    if content:
        for line in content.splitlines():
            match = re.match(r"^(Allow|Disallow):\s*(.*)", line, re.IGNORECASE)
            if match:
                rules.append((match.group(1), match.group(2)))
    return rules

def display_results(domain, content):
    console.print(f"[bold white][*] Checking robots.txt for: {domain}[/bold white]")

    if not content:
        console.print("[bold red][!] No robots.txt found.[/bold red]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Rule Type", style="cyan", justify="left")
    table.add_column("Path", style="green", justify="left")

    rules = parse_crawl_rules(content)
    if rules:
        for rule, path in rules:
            table.add_row(rule, path)
        console.print(table)
    else:
        console.print("[bold yellow][!] No specific crawl rules found.[/bold yellow]")

def main():
    banner()
    url = input("Enter the website URL: ").strip()
    domain, robots_txt = fetch_robots_txt(url)
    display_results(domain, robots_txt)
    console.print("[bold white][*] Crawl rules check completed.[/bold white]")

if __name__ == "__main__":
    main()
