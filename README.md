# Outris CLI

Natural language CLI for any API. Register your APIs, query them with plain English, collaborate with your team.

## Installation

```bash
# Install with pip
pip install outris

# Or with Poetry
poetry add outris
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
outris add-api ./openapi.yaml --visibility org
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
- `outris api add-secret <api-name>` - Store encrypted credentials
- `outris api list` - List registered APIs

### Querying
- `outris ask "query"` - Query APIs with natural language
- `outris query interactive` - Start interactive session
- `outris query history` - Show recent queries

### Team Collaboration
- `outris team invite <email>` - Invite team member
- `outris team list` - List team members

### Marketplace
- `outris marketplace browse` - Browse public APIs
- `outris marketplace install <api-name>` - Add public API to your org

## Development

```bash
# Clone repo
git clone https://github.com/outris/cli
cd outris-cli

# Install dependencies
poetry install

# Run in dev mode with mock backend
export OUTRIS_USE_MOCK=true
poetry run outris --help

# Test signup flow
poetry run outris signup
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

## Environment Variables

- `OUTRIS_USE_MOCK` - Use mock backend (default: `true` for development)
- `OUTRIS_API_URL` - Backend API URL (default: `https://outris-api.railway.app`)

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=outris

# Run specific test file
poetry run pytest tests/test_auth.py
```

## License

MIT
