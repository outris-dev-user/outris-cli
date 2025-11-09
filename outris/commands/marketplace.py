"""
Marketplace commands: browse, install
"""

import typer
from rich.console import Console
from rich.table import Table

from outris.client import create_client

app = typer.Typer()
console = Console()

@app.command()
def browse(
    category: str = typer.Option("", help="Filter by category"),
):
    """Browse public API marketplace"""
    
    client = create_client()
    result = client.get_marketplace()
    
    table = Table(title="API Marketplace")
    table.add_column("Name", style="cyan")
    table.add_column("Category", style="yellow")
    table.add_column("Installs", justify="right", style="green")
    
    apis = result['apis']
    
    # Filter by category if specified
    if category:
        apis = [a for a in apis if a['category'].lower() == category.lower()]
    
    for api in apis:
        table.add_row(
            api['name'],
            api['category'],
            str(api['installs'])
        )
    
    console.print(table)
    console.print(f"\n[dim]Total: {len(apis)} APIs[/dim]")
    console.print("\nInstall with: [cyan]outris marketplace install <api-name>[/cyan]")

@app.command()
def install(
    api_name: str = typer.Argument(..., help="API name to install"),
):
    """Install public API from marketplace"""
    
    client = create_client()
    
    with console.status(f"Installing {api_name}..."):
        result = client.install_from_marketplace(api_name)
    
    console.print(f"[green]✓[/green] {result['message']}")
    console.print(f"[dim]API ID: {result['api_id']}[/dim]")
    console.print(f"\nYou can now query this API:")
    console.print(f"  [cyan]outris ask \"your query\"[/cyan]")
