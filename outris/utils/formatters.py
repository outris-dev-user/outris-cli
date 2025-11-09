"""
Output formatting utilities
"""

from rich.console import Console
from rich.table import Table
from typing import Any, Dict, List

console = Console()

def format_json(data: Dict[str, Any]):
    """Format JSON output with syntax highlighting"""
    console.print_json(data=data)

def format_table(data: List[Dict[str, Any]], title: str = "Results"):
    """Format list of dicts as table"""
    if not data:
        console.print("[yellow]No data to display[/yellow]")
        return
    
    table = Table(title=title)
    
    # Add columns from first item
    for key in data[0].keys():
        table.add_column(key.replace('_', ' ').title(), style="cyan")
    
    # Add rows
    for item in data:
        table.add_row(*[str(v) for v in item.values()])
    
    console.print(table)
