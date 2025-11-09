"""
API management commands: add, add-secret, list
"""

import typer
import yaml
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

from outris.client import create_client

app = typer.Typer()
console = Console()

@app.command()
def add(
    spec_path: str = typer.Argument(..., help="Path to OpenAPI spec (YAML/JSON)"),
    visibility: str = typer.Option("org", help="Visibility: private, org, public"),
    name: str = typer.Option("", help="Custom API name"),
):
    """Register new API from OpenAPI specification"""
    
    # Load spec file
    spec_file = Path(spec_path)
    if not spec_file.exists():
        console.print(f"[red]✗[/red] File not found: {spec_path}")
        raise typer.Exit(1)
    
    with open(spec_file) as f:
        if spec_path.endswith('.yaml') or spec_path.endswith('.yml'):
            spec = yaml.safe_load(f)
        else:
            import json
            spec = json.load(f)
    
    # Extract name from spec if not provided
    if not name:
        name = spec.get('info', {}).get('title', spec_file.stem)
    
    # Register API
    client = create_client()
    
    with console.status(f"Registering {name}..."):
        result = client.register_api(spec, name, visibility)
    
    console.print(f"\n[green]✓[/green] API registered: [cyan]{result['name']}[/cyan]")
    console.print(f"  Endpoints discovered: [cyan]{result['endpoints']}[/cyan]")
    console.print(f"  Intent mappings generated: [cyan]{result['intent_mappings']}[/cyan]")
    console.print(f"  Visibility: [cyan]{visibility}[/cyan]")
    
    # Optionally add secrets
    if Confirm.ask("\nAdd API credentials?"):
        add_secret(result['name'])

@app.command()
def add_secret(
    api_name: str = typer.Argument(..., help="API name"),
    key_name: str = typer.Option("", help="Secret name (e.g., API_KEY)"),
):
    """Store encrypted API credentials"""
    
    if not key_name:
        key_name = Prompt.ask("Secret name (e.g., STRIPE_API_KEY)")
    
    value = Prompt.ask("Secret value", password=True)
    
    client = create_client()
    
    with console.status("Encrypting and storing secret..."):
        result = client.add_secret(api_name, key_name, value)
    
    console.print(f"[green]✓[/green] {result['message']}")
    console.print("[dim]Secret encrypted and available to all team members[/dim]")

@app.command()
def list(
    scope: str = typer.Option("all", help="Scope: all, org, public"),
):
    """List registered APIs"""
    
    client = create_client()
    result = client.list_apis(scope)
    
    if result['count'] == 0:
        console.print("[yellow]No APIs found[/yellow]")
        console.print("\nAdd an API: [cyan]outris add-api <spec.yaml>[/cyan]")
        return
    
    table = Table(title=f"APIs ({scope})")
    table.add_column("Name", style="cyan")
    table.add_column("Visibility", style="yellow")
    table.add_column("Endpoints", justify="right", style="green")
    
    for api in result['apis']:
        table.add_row(
            api['name'],
            api['visibility'],
            str(api['endpoints'])
        )
    
    console.print(table)
    console.print(f"\n[dim]Total: {result['count']} APIs[/dim]")
