"""
Query commands: ask, interactive, history
"""

import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.syntax import Syntax
import json

from outris.client import create_client

app = typer.Typer()
console = Console()

@app.command()
def ask(
    query_text: str = typer.Argument(..., help="Natural language query"),
    output: str = typer.Option("pretty", help="Output format: pretty, json, table"),
):
    """Query APIs using natural language"""
    
    console.print(f"\n[bold blue]Processing:[/bold blue] {query_text}\n")
    
    client = create_client()
    
    with console.status("Executing query..."):
        result = client.query(query_text)
    
    if output == "json":
        console.print_json(data=result)
    elif output == "pretty":
        _render_pretty(result)
    elif output == "table":
        _render_table(result)

def _render_pretty(result: dict):
    """Render query result with Rich formatting"""
    
    # Main result
    if 'result' in result:
        console.print(Panel(
            Syntax(json.dumps(result['result'], indent=2), "json"),
            title="Result",
            border_style="green"
        ))
    
    # Metadata
    console.print(f"\n[dim]API used:[/dim] [cyan]{result.get('api_used', 'N/A')}[/cyan]")
    console.print(f"[dim]Response time:[/dim] [cyan]{result.get('execution_time_ms', 0)}ms[/cyan]")
    
    if 'cost' in result:
        console.print(f"[dim]Cost:[/dim] [cyan]${result['cost']:.4f}[/cyan]")

def _render_table(result: dict):
    """Render query result as table (for list results)"""
    from rich.table import Table
    
    # This is a simplified version - expand based on result structure
    table = Table(title="Query Result")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="yellow")
    
    for key, value in result.get('result', {}).items():
        table.add_row(str(key), str(value))
    
    console.print(table)

@app.command()
def interactive():
    """Start interactive CLI session"""
    
    console.print("\n[bold]Outris Interactive Mode[/bold]")
    console.print("Type [cyan]exit[/cyan] to quit, [cyan]help[/cyan] for commands\n")
    
    client = create_client()
    
    while True:
        try:
            query_text = Prompt.ask("[bold cyan]outris>[/bold cyan]")
            
            if query_text.lower() == "exit":
                console.print("[dim]Goodbye![/dim]")
                break
            elif query_text.lower() == "help":
                console.print("\n[bold]Available commands:[/bold]")
                console.print("  [cyan]exit[/cyan] - Quit interactive mode")
                console.print("  [cyan]help[/cyan] - Show this message")
                console.print("  [cyan]<any query>[/cyan] - Execute natural language query\n")
                continue
            
            result = client.query(query_text)
            _render_pretty(result)
            console.print()  # Blank line
            
        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye![/dim]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")

@app.command()
def history(
    limit: int = typer.Option(10, help="Number of recent queries to show"),
):
    """Show recent query history"""
    
    client = create_client()
    result = client.get_history(limit)
    
    from rich.table import Table
    
    table = Table(title="Query History")
    table.add_column("Query", style="cyan")
    table.add_column("API", style="yellow")
    table.add_column("Timestamp", style="dim")
    
    for query in result['queries']:
        table.add_row(
            query['query'],
            query['api'],
            query['timestamp']
        )
    
    console.print(table)
