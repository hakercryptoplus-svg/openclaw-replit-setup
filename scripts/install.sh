#!/bin/bash
# OpenClaw Install Script for Replit
set -e

echo "=== OpenClaw Install Script ==="
echo "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2)"
echo "Node: $(node --version)"

# Setup pnpm
export PNPM_HOME="/home/runner/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"

# Install openclaw globally
echo "[1/4] Installing openclaw..."
pnpm add -g openclaw@latest

# Create config directory
echo "[2/4] Setting up config..."
mkdir -p ~/.openclaw

# Copy openclaw.json template (replace env var placeholders)
cp openclaw.json.template ~/.openclaw/openclaw.json
cp SOUL.md ~/.openclaw/SOUL.md

# Copy environment docs for agent knowledge
cp REPLIT_ENVIRONMENT.md ~/.openclaw/REPLIT_ENVIRONMENT.md

# Check required secrets
echo "[3/4] Checking secrets..."
missing=""
[ -z "$PORTKEY_API_KEY" ] && missing="$missing PORTKEY_API_KEY"
[ -z "$TELEGRAM_BOT_TOKEN" ] && missing="$missing TELEGRAM_BOT_TOKEN"

if [ -n "$missing" ]; then
    echo "ERROR: Missing secrets:$missing"
    echo "Add them in Replit Secrets tab, then re-run."
    exit 1
fi

echo "[4/4] Done! OpenClaw workflow will start automatically."
echo ""
echo "To start manually:"
echo "  export PNPM_HOME=\"/home/runner/.local/share/pnpm\""
echo "  export PATH=\"\$PNPM_HOME:\$PATH\""
echo "  openclaw gateway run --force --allow-unconfigured"
