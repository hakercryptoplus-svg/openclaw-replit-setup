#!/bin/bash
set -e
echo "=== OpenClaw + LiteLLM Install ==="
export PNPM_HOME="/home/runner/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"

echo "[1/4] Installing openclaw..."
pnpm add -g openclaw@latest

echo "[2/4] Installing LiteLLM..."
pip install "litellm[proxy]"

echo "[3/4] Setting up openclaw config..."
mkdir -p ~/.openclaw/workspace
cp openclaw.json.template ~/.openclaw/openclaw.json
cp SOUL.md ~/.openclaw/workspace/SOUL.md
cp REPLIT_ENVIRONMENT.md ~/.openclaw/REPLIT_ENVIRONMENT.md

echo "[4/4] Patching openclaw: LiteLLM + Telegram allowlist..."
# Replace YOUR_TELEGRAM_CHAT_ID_NUMBER with your actual Telegram user ID (numeric)
CHAT_ID="${TELEGRAM_CHAT_ID:-7281928709}"
cat > /tmp/openclaw_patch.json << PATCH
{
  "models": {"providers": {"litellm": {"baseUrl": "http://127.0.0.1:4000/v1","apiKey": "sk-litellm-local","api": "openai-completions","models": [{"id": "gemini-3.5-flash","name": "Gemini 3.5 Flash","reasoning": false,"input": ["text","image"],"contextWindow": 1000000,"maxTokens": 64000}]}}},
  "agents": {"defaults": {"model": {"primary": "litellm/gemini-3.5-flash"}}},
  "channels": {"telegram": {"dmPolicy": "allowlist","groupPolicy": "disabled","allowFrom": [$CHAT_ID]}}
}
PATCH

openclaw config patch --stdin < /tmp/openclaw_patch.json

echo ""
echo "Done! Telegram allowlist set for chat ID: $CHAT_ID"
echo "No pairing needed on restart."
echo ""
echo "First run: start LiteLLM then OpenClaw (Replit workflows handle this automatically)"
