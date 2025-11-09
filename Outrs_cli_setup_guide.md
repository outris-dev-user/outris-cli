# Query: 
# ContextLines: 1

# Outris CLI - New Repository Setup Guide

**Date:** November 9, 2025  
**Purpose:** Bootstrap `outris-cli` as separate Python CLI project  
**Timeline:** 3 weeks to MVP  
**Dependencies:** Backend API at `ai-api-orchestrator` (parallel development)

---

## Quick Start (5 Minutes)

```bash
# 1. Create new repo
mkdir outris-cli
cd outris-cli
git init

# 2. Initialize Poetry
poetry init --name outris --description "Natural language CLI for any API"

# 3. Add dependencies
poetry add typer rich requests pydantic pyyaml keyring
poetry add --group dev pytest black mypy

# 4. Create project structure
mkdir -p outris/{commands,utils}
touch outris/__init__.py
touch outris/main.py
touch outris/client.py
touch outris/config.py
touch README.md

# 5. Install and test
poetry install
poetry run outris --help
```

---

## Complete Project Structure

```
outris-cli/
├── .gitignore
├── README.md
├── LICENSE (MIT)
├── pyproject.toml
├── poetry.lock
├── outris/
│   ├── __init__.py
│   ├── main.py              # Typer app entry point
│   ├── client.py            # Backend API client (mock + real)
│   ├── config.py            # ~/.outris/config.json management
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── auth.py          # signup, login, logout
│   │   ├── api.py           # add-api, add-secret, list-apis
│   │   ├── query.py         # ask, interactive
│   │   ├── team.py          # invite, accept-invite, list-team
│   │   └── marketplace.py   # marketplace, install
│   └── utils/
│       ├── __init__.py
│       ├── formatters.py    # Rich output formatting
│       └── validators.py    # Input validation
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_api.py
│   └── test_client.py
└── docs/
    ├── installation.md
    ├── quickstart.md
    └── commands.md
```

---

## File Templates (Copy-Paste Ready)

### 1. `pyproject.toml`

```toml
[tool.poetry]
name = "outris"
version = "0.1.0"
description = "Natural language CLI for any API - register, query, and collaborate"
authors = ["Outris Team <hello@outris.dev>"]
readme = "README.md"
homepage = "https://outris.dev"
repository = "https://github.com/outris/cli"
keywords = ["api", "cli", "openapi", "natural-language", "llm"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

[tool.poetry.dependencies]
python = "^3.9"
typer = "^0.9.0"
rich = "^13.0.0"
requests = "^2.31.0"
pydantic = "^2.0.0"
pyyaml = "^6.0"
keyring = "^24.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.0.0"
mypy = "^1.5.0"
pytest-cov = "^4.1.0"

[tool.poetry.scripts]
outris = "outris.main:app"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

### 2. `outris/__init__.py`

```python
"""
Outris CLI - Natural language interface for any API
"""

__version__ = "0.1.0"
__author__ = "Outris Team"
__email__ = "hello@outris.dev"
```

---

### 3. `outris/main.py`

```python
"""
Main entry point for Outris CLI
"""

import typer
from rich.console import Console

from outris.commands import auth, api, query, team, marketplace

app = typer.Typer(
    name="outris",
    help="Natural language CLI for any API",
    add_completion=True,
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
    """Create new account (alias for auth signup)"""
    auth.signup()

@app.command()
def login():
    """Login with OTP (alias for auth login)"""
    auth.login()

@app.command()
def ask(
    query: str = typer.Argument(..., help="Natural language query"),
    output: str = typer.Option("pretty", help="Output format: pretty, json, table"),
):
    """Query APIs using natural language (alias for query ask)"""
    query.ask(query, output)

@app.command()
def add_api(
    spec_path: str = typer.Argument(..., help="Path to OpenAPI spec"),
    visibility: str = typer.Option("org", help="Visibility: private, org, public"),
    name: str = typer.Option(None, help="Custom API name"),
):
    """Register new API (alias for api add)"""
    api.add_api(spec_path, visibility, name)

@app.callback()
def main():
    """
    Outris CLI - Natural language interface for any API
    
    Register your APIs, query them with plain English, collaborate with your team.
    """
    pass

if __name__ == "__main__":
    app()
```

---

### 4. `outris/config.py`

```python
"""
Configuration management for Outris CLI
Stores API key, org info in ~/.outris/config.json
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

CONFIG_DIR = Path.home() / ".outris"
CONFIG_FILE = CONFIG_DIR / "config.json"

def ensure_config_dir():
    """Create ~/.outris directory if it doesn't exist"""
    CONFIG_DIR.mkdir(exist_ok=True)

def load_config() -> Dict[str, Any]:
    """Load configuration from ~/.outris/config.json"""
    if not CONFIG_FILE.exists():
        return {}
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config: Dict[str, Any]):
    """Save configuration to ~/.outris/config.json"""
    ensure_config_dir()
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_api_key() -> Optional[str]:
    """Get stored API key"""
    config = load_config()
    return config.get("api_key")

def get_org_id() -> Optional[str]:
    """Get stored org ID"""
    config = load_config()
    return config.get("org_id")

def clear_config():
    """Clear stored configuration (logout)"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
```

---

### 5. `outris/client.py`

```python
"""
Backend API client - supports mock and real backends
"""

import os
import requests
from typing import Dict, Any, Protocol
from outris.config import get_api_key

class BackendClient(Protocol):
    """Interface for backend clients"""
    def signup(self, email: str, org_name: str) -> Dict[str, Any]: ...
    def verify_otp(self, email: str, otp: str) -> Dict[str, Any]: ...
    def login(self, email: str) -> Dict[str, Any]: ...
    def register_api(self, spec: Dict, name: str, visibility: str) -> Dict[str, Any]: ...
    def add_secret(self, api_name: str, key_name: str, value: str) -> Dict[str, Any]: ...
    def list_apis(self, scope: str = "all") -> Dict[str, Any]: ...
    def query(self, query_text: str) -> Dict[str, Any]: ...
    def get_history(self, limit: int = 10) -> Dict[str, Any]: ...
    def invite_member(self, email: str, role: str) -> Dict[str, Any]: ...
    def accept_invitation(self, token: str, email: str, otp: str) -> Dict[str, Any]: ...
    def list_team(self) -> Dict[str, Any]: ...
    def get_marketplace(self) -> Dict[str, Any]: ...
    def install_from_marketplace(self, api_name: str) -> Dict[str, Any]: ...


class MockBackendClient:
    """Mock client for development when backend isn't ready"""
    
    def signup(self, email: str, org_name: str) -> Dict[str, Any]:
        return {
            "message": "OTP sent to email (MOCKED)",
            "expires_in": 300
        }
    
    def verify_otp(self, email: str, otp: str) -> Dict[str, Any]:
        return {
            "api_key": "sk_outris_mock_abc123",
            "org_id": "org_mock_123",
            "org_name": email.split('@')[0],
            "email": email
        }
    
    def login(self, email: str) -> Dict[str, Any]:
        return {
            "message": "OTP sent to email (MOCKED)",
            "expires_in": 300
        }
    
    def register_api(self, spec: Dict, name: str, visibility: str) -> Dict[str, Any]:
        return {
            "api_id": "api_mock_456",
            "name": name,
            "endpoints": len(spec.get("paths", {})),
            "intent_mappings": 10,
            "visibility": visibility
        }
    
    def add_secret(self, api_name: str, key_name: str, value: str) -> Dict[str, Any]:
        return {
            "message": f"Secret {key_name} stored (MOCKED)"
        }
    
    def list_apis(self, scope: str = "all") -> Dict[str, Any]:
        return {
            "count": 3,
            "apis": [
                {"name": "Mock Weather API", "visibility": "public", "endpoints": 5},
                {"name": "Mock Payment API", "visibility": "org", "endpoints": 12},
                {"name": "Mock Analytics API", "visibility": "private", "endpoints": 8},
            ]
        }
    
    def query(self, query_text: str) -> Dict[str, Any]:
        return {
            "result": {
                "message": f"Mock result for: {query_text}",
                "data": {"temperature": 72, "condition": "sunny"}
            },
            "api_used": "Mock Weather API",
            "execution_time_ms": 123,
            "cost": 0.001
        }
    
    def get_history(self, limit: int = 10) -> Dict[str, Any]:
        return {
            "count": 2,
            "queries": [
                {"query": "get weather in SF", "api": "Mock Weather", "timestamp": "2025-11-09T10:30:00Z"},
                {"query": "create charge $50", "api": "Mock Payment", "timestamp": "2025-11-09T09:15:00Z"},
            ]
        }
    
    def invite_member(self, email: str, role: str) -> Dict[str, Any]:
        return {"message": f"Invitation sent to {email} (MOCKED)"}
    
    def accept_invitation(self, token: str, email: str, otp: str) -> Dict[str, Any]:
        return {
            "api_key": "sk_outris_mock_xyz789",
            "org_id": "org_mock_123",
            "role": "member"
        }
    
    def list_team(self) -> Dict[str, Any]:
        return {
            "count": 3,
            "members": [
                {"email": "alice@acme.com", "role": "owner"},
                {"email": "bob@acme.com", "role": "admin"},
                {"email": "charlie@acme.com", "role": "member"},
            ]
        }
    
    def get_marketplace(self) -> Dict[str, Any]:
        return {
            "count": 5,
            "apis": [
                {"name": "OpenWeatherMap", "installs": 1234, "category": "Weather"},
                {"name": "SendGrid", "installs": 890, "category": "Email"},
                {"name": "Twilio", "installs": 756, "category": "SMS"},
                {"name": "Stripe Demo", "installs": 456, "category": "Payments"},
                {"name": "Google Maps", "installs": 2341, "category": "Maps"},
            ]
        }
    
    def install_from_marketplace(self, api_name: str) -> Dict[str, Any]:
        return {
            "message": f"{api_name} added to your org (MOCKED)",
            "api_id": "api_marketplace_123"
        }


class RealBackendClient:
    """Real HTTP client for deployed backend"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv(
            "OUTRIS_API_URL",
            "https://outris-api.railway.app"
        )
    
    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with auth"""
        url = f"{self.base_url}{path}"
        
        # Add API key header if available
        api_key = get_api_key()
        if api_key:
            kwargs.setdefault('headers', {})
            kwargs['headers']['X-API-Key'] = api_key
        
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def signup(self, email: str, org_name: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/auth/signup', json={
            "email": email,
            "org_name": org_name
        })
    
    def verify_otp(self, email: str, otp: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/auth/verify-otp', json={
            "email": email,
            "otp": otp
        })
    
    def login(self, email: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/auth/login', json={
            "email": email
        })
    
    def register_api(self, spec: Dict, name: str, visibility: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/apis/register', json={
            "spec": spec,
            "name": name,
            "visibility": visibility
        })
    
    def add_secret(self, api_name: str, key_name: str, value: str) -> Dict[str, Any]:
        # First get API ID from name
        apis = self.list_apis(scope="org")
        api_id = next((a['api_id'] for a in apis['apis'] if a['name'] == api_name), None)
        
        if not api_id:
            raise ValueError(f"API '{api_name}' not found")
        
        return self._request('POST', f'/api/v1/apis/{api_id}/secrets', json={
            "key_name": key_name,
            "value": value
        })
    
    def list_apis(self, scope: str = "all") -> Dict[str, Any]:
        return self._request('GET', f'/api/v1/apis?scope={scope}')
    
    def query(self, query_text: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/query', json={
            "query": query_text
        })
    
    def get_history(self, limit: int = 10) -> Dict[str, Any]:
        return self._request('GET', f'/api/v1/history?limit={limit}')
    
    def invite_member(self, email: str, role: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/team/invite', json={
            "email": email,
            "role": role
        })
    
    def accept_invitation(self, token: str, email: str, otp: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/team/accept', json={
            "token": token,
            "email": email,
            "otp": otp
        })
    
    def list_team(self) -> Dict[str, Any]:
        return self._request('GET', '/api/v1/team/members')
    
    def get_marketplace(self) -> Dict[str, Any]:
        return self._request('GET', '/api/v1/marketplace')
    
    def install_from_marketplace(self, api_name: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v1/marketplace/install', json={
            "api_name": api_name
        })


def create_client(use_mock: bool = None) -> BackendClient:
    """
    Factory function to create appropriate client
    
    Use mock if:
    - Explicitly requested via use_mock=True
    - Environment variable OUTRIS_USE_MOCK is set
    - Backend not ready (development mode)
    """
    if use_mock is None:
        use_mock = os.getenv("OUTRIS_USE_MOCK", "false").lower() == "true"
    
    if use_mock:
        return MockBackendClient()
    else:
        return RealBackendClient()
```

---

### 6. `outris/commands/auth.py`

```python
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
```

---

### 7. `outris/commands/api.py`

```python
"""
API management commands: add-api, add-secret, list-apis
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
    name: str = typer.Option(None, help="Custom API name"),
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
    key_name: str = typer.Option(None, help="Secret name (e.g., API_KEY)"),
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
```

---

### 8. `outris/commands/query.py`

```python
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
    query: str = typer.Argument(..., help="Natural language query"),
    output: str = typer.Option("pretty", help="Output format: pretty, json, table"),
):
    """Query APIs using natural language"""
    
    console.print(f"\n[bold blue]Processing:[/bold blue] {query}\n")
    
    client = create_client()
    
    with console.status("Executing query..."):
        result = client.query(query)
    
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
            query = Prompt.ask("[bold cyan]outris>[/bold cyan]")
            
            if query.lower() == "exit":
                console.print("[dim]Goodbye![/dim]")
                break
            elif query.lower() == "help":
                console.print("\n[bold]Available commands:[/bold]")
                console.print("  [cyan]exit[/cyan] - Quit interactive mode")
                console.print("  [cyan]help[/cyan] - Show this message")
                console.print("  [cyan]<any query>[/cyan] - Execute natural language query\n")
                continue
            
            result = client.query(query)
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
```

---

### 9. `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# Poetry
poetry.lock

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Outris config (local testing)
.outris/
```

---

### 10. `README.md`

```markdown
# Outris CLI

Natural language CLI for any API. Register your APIs, query them with plain English, collaborate with your team.

## Installation

```bash
pip install outris
```

Or with Homebrew (coming soon):

```bash
brew install outris
```

## Quick Start

### 1. Create Account

```bash
outris signup
# Enter email and org name
# Verify OTP from email
```

### 2. Add Your API

```bash
outris add-api ./stripe-api.yaml --visibility org
# Optionally add API credentials
```

### 3. Query with Natural Language

```bash
outris ask "create a $50 charge for customer cus_123"
```

### 4. Invite Your Team

```bash
outris invite bob@yourcompany.com
```

## Commands

### Authentication
- `outris signup` - Create new account
- `outris login` - Login with OTP
- `outris logout` - Clear credentials
- `outris auth status` - Show current user

### API Management
- `outris add-api <spec.yaml>` - Register API from OpenAPI spec
- `outris add-secret <api-name> <key-name>` - Store encrypted credentials
- `outris api list` - List registered APIs

### Querying
- `outris ask "query"` - Query APIs with natural language
- `outris query interactive` - Start interactive session
- `outris query history` - Show recent queries

### Team Collaboration
- `outris invite <email>` - Invite team member
- `outris team list` - List team members

### Marketplace
- `outris marketplace` - Browse public APIs
- `outris marketplace install <api-name>` - Add public API to your org

## Output Formats

```bash
outris ask "query" --output json    # JSON output
outris ask "query" --output pretty  # Rich formatted (default)
outris ask "query" --output table   # Table format
```

## Configuration

Config stored in `~/.outris/config.json`:

```json
{
  "api_key": "sk_outris_...",
  "email": "you@example.com",
  "org_id": "org_...",
  "org_name": "Your Org"
}
```

## Development

```bash
# Clone repo
git clone https://github.com/outris/cli
cd outris-cli

# Install dependencies
poetry install

# Run in dev mode
poetry run outris --help

# Use mock backend
export OUTRIS_USE_MOCK=true
poetry run outris signup
```

## License

MIT
```

---

## Development Workflow

### Week 1: Mock Development

```bash
# Enable mock mode
export OUTRIS_USE_MOCK=true

# Test all commands without backend
poetry run outris signup
poetry run outris add-api ./test-api.yaml
poetry run outris ask "test query"
poetry run outris api list
```

### Week 2: Backend Integration

```bash
# Point to real backend
export OUTRIS_API_URL=https://outris-api.railway.app
export OUTRIS_USE_MOCK=false

# Test with real backend
poetry run outris signup
# (use real email, get OTP)
```

### Week 3: Publishing

```bash
# Build package
poetry build

# Test publish (PyPI test)
poetry publish --repository testpypi

# Real publish
poetry publish
```

---

## Testing Commands

```bash
# Run tests
poetry run pytest

# With coverage
poetry run pytest --cov=outris

# Type checking
poetry run mypy outris/

# Formatting
poetry run black outris/
```

---

## Next Steps

1. **Copy all files above** into new `outris-cli` repo
2. **Run `poetry install`** to set up environment
3. **Test with mock**: `export OUTRIS_USE_MOCK=true && poetry run outris signup`
4. **Implement remaining commands** (team.py, marketplace.py)
5. **Add tests** for each command
6. **Wait for backend** to be ready, then switch to real client

---

## Backend API Contract

The CLI expects these endpoints:

```
POST /api/v1/auth/signup          - Send OTP
POST /api/v1/auth/verify-otp      - Verify OTP, get API key
POST /api/v1/auth/login           - Send OTP to existing user
POST /api/v1/apis/register        - Register API
POST /api/v1/apis/{id}/secrets    - Add secret
GET  /api/v1/apis?scope=all       - List APIs
POST /api/v1/query                - Execute query
GET  /api/v1/history?limit=10     - Get history
POST /api/v1/team/invite          - Invite member
POST /api/v1/team/accept          - Accept invite
GET  /api/v1/team/members         - List team
GET  /api/v1/marketplace          - Browse marketplace
POST /api/v1/marketplace/install  - Install from marketplace
```

All protected endpoints require `X-API-Key` header.

---

## Questions?

- GitHub: https://github.com/outris/cli
- Docs: https://outris.dev/docs
- Email: hello@outris.dev
