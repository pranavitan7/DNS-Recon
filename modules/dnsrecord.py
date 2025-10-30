import subprocess
from rich.console import Console
from rich.table import Table
from rich import box

console = Console() 

# Define colors for different record types
record_colors = {
    "A": "cyan",
    "AAAA": "blue",
    "MX": "magenta",
    "NS": "green",
    "TXT": "yellow",
    "SOA": "red",
}

def get_dns_records(domain):
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA"]
    records = {}

    for record in record_types:
        try:
            result = subprocess.run(
                ["dig", record, domain, "+short", "@8.8.8.8"],  # Corrected syntax
                capture_output=True,
                text=True,
                timeout=10  # Prevents hanging
            )

            if result.returncode != 0:
                records[record] = f"[red]Error: {result.stderr.strip()}[/red]"
                continue

            output = result.stdout.strip()
            records[record] = output if output else "[yellow]No records found[/yellow]"

        except subprocess.TimeoutExpired:
            records[record] = "[red]Lookup Timed Out[/red]"
        except Exception as e:
            records[record] = f"[red]Error: {e}[/red]"

    return records

def display_table(domain, records):
    table = Table(title=f"DNS Records for {domain}", box=box.SQUARE)
    table.add_column("Record Type", style="bold white", justify="left")
    table.add_column("Record Value", style="bold green", justify="left")

    for record, value in records.items():
        color = record_colors.get(record, "white")
        table.add_row(f"[{color}]{record}[/{color}]", value)

    console.print(table)

if __name__ == "__main__":
    domain = input("Enter domain: ").strip()
    console.print(f"\n[bold cyan]Fetching DNS records for:[/bold cyan] [bold white]{domain}[/bold white]\n")
    records = get_dns_records(domain)
    display_table(domain, records)
