"""
Team collaboration commands: invite, accept, list
"""

import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from outris.client import create_client

app = typer.Typer()
console = Console()

@app.command()
def invite(
    email: str = typer.Argument(..., help="Email address to invite"),
    role: str = typer.Option("member", help="Role: admin, member"),
):
    """Invite team member"""
    
    client = create_client()
    
    with console.status(f"Sending invitation to {email}..."):
        result = client.invite_member(email, role)
    
    console.print(f"[green]✓[/green] {result['message']}")
    console.print(f"[dim]Role: {role}[/dim]")

@app.command()
def accept(
    token: str = typer.Argument(..., help="Invitation token from email"),
    email: str = typer.Option("", help="Your email address"),
):
    """Accept team invitation"""
    
    if not email:
        email = Prompt.ask("Your email address")
    
    console.print(f"\n[bold]Accept Team Invitation[/bold]\n")
    console.print(f"Email: {email}")
    
    client = create_client()
    
    # Request OTP
    with console.status("Sending verification code..."):
        # In real implementation, backend sends OTP
        pass
    
    otp = Prompt.ask("Enter 6-digit code from email")
    
    with console.status("Verifying and joining team..."):
        result = client.accept_invitation(token, email, otp)
    
    # Save new config
    from outris.config import save_config
    save_config({
        "api_key": result["api_key"],
        "email": email,
        "org_id": result["org_id"],
        "role": result["role"]
    })
    
    console.print(f"\n[green]✓[/green] Joined team!")
    console.print(f"  Role: [cyan]{result['role']}[/cyan]")

@app.command()
def list():
    """List team members"""
    
    client = create_client()
    result = client.list_team()
    
    table = Table(title="Team Members")
    table.add_column("Email", style="cyan")
    table.add_column("Role", style="yellow")
    
    for member in result['members']:
        table.add_row(
            member['email'],
            member['role']
        )
    
    console.print(table)
    console.print(f"\n[dim]Total: {result['count']} members[/dim]")
