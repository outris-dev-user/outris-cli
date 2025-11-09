#!/bin/bash

echo "Setting up Outris CLI..."

# Install Poetry if not present
if ! command -v poetry &> /dev/null; then
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

# Enable mock mode for development
export OUTRIS_USE_MOCK=true

echo ""
echo "✓ Setup complete!"
echo ""
echo "Try these commands:"
echo "  poetry run outris --help"
echo "  poetry run outris signup"
echo "  poetry run outris api list"
echo ""
echo "Mock mode is enabled (OUTRIS_USE_MOCK=true)"
