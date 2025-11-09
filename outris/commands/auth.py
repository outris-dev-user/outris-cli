"""
Authentication commands: signup, login, logout
"""

import typer
from rich.console import Console
from rich.prompt import Prompt

from outris.client import create_client
from outris.config import save_config, clear_config, load_config

app = typer.Typer()
console = Console()

@app.command()
def signup():
    """Create new account with OTP verification"""
    console.print("\n[bold]Create Outris Account[/bold]\n")
    
    email = Prompt.ask("Email address")
    org_name = Prompt.ask("Organization name")
    
    client = create_client()
    
    # Request OTP
    with console.status(f"Sending OTP to {email}..."):
        result = client.signup(email, org_name)
    
    console.print(f"[green]✓[/green] {result['message']}")
    console.print(f"[dim]Code expires in {result['expires_in']} seconds[/dim]\n")
    
    # Verify OTP
    otp = Prompt.ask("Enter 6-digit code from email")
    
    with console.status("Verifying code..."):
        result = client.verify_otp(email, otp)
    
    # Save config
    save_config({
        "api_key": result["api_key"],
        "email": result["email"],
        "org_id": result["org_id"],
        "org_name": result["org_name"]
    })
    
    console.print(f"\n[green]✓[/green] Account created!")
    console.print(f"  Organization: [cyan]{result['org_name']}[/cyan]")
    console.print(f"  Email: [cyan]{result['email']}[/cyan]")
    console.print(f"\n[dim]API key saved to ~/.outris/config.json[/dim]")
    console.print("\n[bold]Get started:[/bold]")
    console.print("  outris add-api <spec.yaml>")
    console.print("  outris ask \"your query\"")

@app.command()
def login():
    """Login with OTP"""
    console.print("\n[bold]Login to Outris[/bold]\n")
    
    email = Prompt.ask("Email address")
    
    client = create_client()
    
    # Request OTP
    with console.status(f"Sending OTP to {email}..."):
        result = client.login(email)
    
    console.print(f"[green]✓[/green] {result['message']}")
    console.print(f"[dim]Code expires in {result['expires_in']} seconds[/dim]\n")
    
    # Verify OTP
    otp = Prompt.ask("Enter 6-digit code")
    
    with console.status("Verifying code..."):
        result = client.verify_otp(email, otp)
    
    # Save config
    save_config({
        "api_key": result["api_key"],
        "email": result["email"],
        "org_id": result["org_id"],
        "org_name": result.get("org_name", "")
    })
    
    console.print(f"\n[green]✓[/green] Logged in as [cyan]{result['email']}[/cyan]")
    console.print(f"  Organization: [cyan]{result.get('org_name', 'N/A')}[/cyan]")

@app.command()
def logout():
    """Logout and clear stored credentials"""
    config = load_config()
    
    if not config:
        console.print("[yellow]⚠[/yellow] Not logged in")
        return
    
    clear_config()
    console.print("[green]✓[/green] Logged out successfully")
    console.print("[dim]Credentials cleared from ~/.outris/config.json[/dim]")

@app.command()
def status():
    """Show current authentication status"""
    config = load_config()
    
    if not config:
        console.print("[yellow]⚠[/yellow] Not logged in")
        console.print("\nRun: [cyan]outris signup[/cyan] or [cyan]outris login[/cyan]")
        return
    
    console.print("\n[bold]Authentication Status[/bold]\n")
    console.print(f"  Email: [cyan]{config.get('email', 'N/A')}[/cyan]")
    console.print(f"  Organization: [cyan]{config.get('org_name', 'N/A')}[/cyan]")
    console.print(f"  Org ID: [dim]{config.get('org_id', 'N/A')}[/dim]")
    console.print(f"  API Key: [dim]{config.get('api_key', 'N/A')[:20]}...[/dim]")
    console.print(f"\n[green]✓[/green] Logged in")
