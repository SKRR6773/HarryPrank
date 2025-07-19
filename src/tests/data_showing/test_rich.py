from rich.console import Console
from rich.table import Table



console = Console()

console.print("[b green]Hello[/b green]")

table = Table(title="List Client", header_style="cyan")

table.add_column("Name")
table.add_column("Age")
table.add_column("Position")


table.add_row("Frame", str(19), "Programmer")

console.print(table)