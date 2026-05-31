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
echo "[1/5] Installing openclaw..."
pnpm add -g openclaw@latest

# Create config directory
echo "[2/5] Setting up config..."
mkdir -p ~/.openclaw

# Copy config template
cp openclaw.json.template ~/.openclaw/openclaw.json

# Copy SOUL.md to openclaw workspace (created after first run)
mkdir -p ~/.openclaw/workspace
cp SOUL.md ~/.openclaw/workspace/SOUL.md

# Copy environment docs
cp REPLIT_ENVIRONMENT.md ~/.openclaw/REPLIT_ENVIRONMENT.md

# Check required secrets
echo "[3/5] Checking secrets..."
missing=""
[ -z "$PORTKEY_API_KEY" ] && missing="$missing PORTKEY_API_KEY"
[ -z "$TELEGRAM_BOT_TOKEN" ] && missing="$missing TELEGRAM_BOT_TOKEN"

if [ -n "$missing" ]; then
    echo "ERROR: Missing secrets:$missing"
    echo "Add them in Replit Secrets tab, then re-run."
    exit 1
fi

echo "[4/5] Starting gateway to initialize Telegram..."
# Start briefly to init Telegram channel, then stop
timeout 10 openclaw gateway run --force --allow-unconfigured 2>/dev/null || true

echo "[5/5] Approving your Telegram chat ID..."
# Approve your chat ID (send /start to bot first to get pairing code, then run:)
# openclaw pairing approve telegram YOUR_PAIRING_CODE
echo "If you see a pairing code in Telegram, run:"
echo "  openclaw pairing approve telegram <YOUR_PAIRING_CODE>"
echo ""
echo "Done! OpenClaw workflow will start automatically."
echo ""
echo "To start manually:"
echo "  export PNPM_HOME=\"/home/runner/.local/share/pnpm\""
echo "  export PATH=\"$PNPM_HOME:$PATH\""
echo "  openclaw gateway run --force --allow-unconfigured"
