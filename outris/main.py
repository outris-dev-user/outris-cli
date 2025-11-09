"""
Main entry point for Outris CLI
"""

import typer
from rich.console import Console

from outris.commands import auth, api, query, team, marketplace

app = typer.Typer(
    name="outris",
    help="Natural language CLI for any API - register, query, and collaborate",
    no_args_is_help=True,
)

console = Console()

# Register command groups
app.add_typer(auth.app, name="auth", help="Authentication commands")
app.add_typer(api.app, name="api", help="API management commands")
app.add_typer(query.app, name="query", help="Query commands")
app.add_typer(team.app, name="team", help="Team collaboration commands")
app.add_typer(marketplace.app, name="marketplace", help="Marketplace commands")

# Top-level convenience commands (aliases)
@app.command()
def signup():
    """Create new account"""
    from outris.commands import auth as auth_module
    auth_module.signup()

@app.command()
def login():
    """Login with OTP"""
    from outris.commands import auth as auth_module
    auth_module.login()

if __name__ == "__main__":
    app()
