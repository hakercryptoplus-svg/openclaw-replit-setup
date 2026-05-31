# OpenClaw on Replit — Complete Setup

Personal AI assistant via Telegram, powered by Gemini (via Portkey), running on Replit.

## What This Is
- **OpenClaw** gateway running 24/7 on Replit
- **Telegram bot** connected (responds only to your chat ID)
- **Model**: Gemini 3.5 Flash via Portkey proxy
- **No public UI** — headless/private mode

## Quick Start on a New Replit

### 1. Import this repo into Replit
Create a new Replit, choose "Import from GitHub", paste this repo URL.

### 2. Set these secrets in Replit Secrets tab
| Secret | Value |
|--------|-------|
| `PORTKEY_API_KEY` | Your Portkey API key |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |

### 3. Install & run
```bash
bash scripts/install.sh
```
OpenClaw starts automatically via the workflow.

## Files
| File | Purpose |
|------|---------|
| `openclaw.json.template` | OpenClaw config template (copy to `~/.openclaw/openclaw.json`) |
| `SOUL.md` | Agent personality — edit to customize behavior |
| `REPLIT_ENVIRONMENT.md` | Full Replit environment docs for the agent |
| `scripts/install.sh` | One-shot install + setup script |
| `start.sh` | Start script used by Replit workflow |

## Architecture
```
You (Telegram) → OpenClaw Gateway → Portkey → Google Gemini
```

## Replit Workflow Command
```
export PNPM_HOME="/home/runner/.local/share/pnpm" && export PATH="$PNPM_HOME:$PATH" && openclaw gateway run --force --allow-unconfigured
```
