#!/bin/bash
# Outris CLI Aliases - Source this file to use outris commands easily
# Usage: source .outris_aliases.sh

export PATH="/home/codespace/.local/bin:$PATH"
export OUTRIS_USE_MOCK=true

# Create function instead of alias for better compatibility
outris() {
    cd /workspaces/outris-cli && poetry run outris "$@"
}

export -f outris

echo "✅ Outris CLI ready!"
echo "   Run: outris --help"
