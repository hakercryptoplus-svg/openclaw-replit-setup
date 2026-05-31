#!/bin/bash
# OpenClaw Startup Script for Replit
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
[ -z "$TELEGRAM_BOT_TOKEN" ] && missing="$missing TELEGRAM_BOT_TOKEN"
if [ -n "$missing" ]; then
    echo "[openclaw] ERROR: Missing required environment variables:$missing"
    exit 1
fi

echo "[openclaw] Patching config (non-destructive)..."
CHAT_ID="${TELEGRAM_CHAT_ID:-7281928709}"

# Use config patch — preserves existing keys (pairing, commands.ownerAllowFrom, etc.)
cat > /tmp/openclaw_startup_patch.json << PATCH
{
  "models": {
    "providers": {
      "litellm": {
        "baseUrl": "http://127.0.0.1:4000/v1",
        "apiKey": "sk-litellm-local",
        "api": "openai-completions",
        "models": [
          {
            "id": "gemini-3.5-flash",
            "name": "Gemini 3.5 Flash",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 1000000,
            "maxTokens": 64000
          }
        ]
      }
    }
  },
  "agents": {"defaults": {"model": {"primary": "litellm/gemini-3.5-flash"}}},
  "channels": {"telegram": {"dmPolicy": "allowlist", "groupPolicy": "disabled", "allowFrom": [$CHAT_ID]}}
}
PATCH

openclaw config patch --stdin < /tmp/openclaw_startup_patch.json

echo "[openclaw] Starting OpenClaw gateway..."
echo "[openclaw] Model: gemini-3.5-flash via LiteLLM → Portkey"
echo "[openclaw] Telegram: enabled (chat ID: $CHAT_ID)"

exec openclaw gateway run --force --allow-unconfigured
