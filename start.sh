#!/bin/bash
# OpenClaw Startup Script for Replit
# This script starts the OpenClaw gateway with Telegram bot and Portkey/Gemini models

set -e

export PNPM_HOME="/home/runner/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"

# Verify openclaw is installed
if ! command -v openclaw &> /dev/null; then
    echo "[openclaw] Installing openclaw..."
    pnpm add -g openclaw@latest
fi

# Check required env vars
missing=""
[ -z "$PORTKEY_API_KEY" ] && missing="$missing PORTKEY_API_KEY"
[ -z "$TELEGRAM_BOT_TOKEN" ] && missing="$missing TELEGRAM_BOT_TOKEN"

if [ -n "$missing" ]; then
    echo "[openclaw] ERROR: Missing required environment variables:$missing"
    echo "[openclaw] Please set them in Replit Secrets tab."
    exit 1
fi

echo "[openclaw] Starting OpenClaw gateway..."
echo "[openclaw] Model: ${OPENCLAW_MODEL:-gemini-3.5-flash} via Portkey"
echo "[openclaw] Telegram: enabled"
echo "[openclaw] UI: disabled"

# Start openclaw gateway (no UI, headless mode)
exec openclaw gateway:start --no-ui --config /home/runner/.openclaw/openclaw.json
