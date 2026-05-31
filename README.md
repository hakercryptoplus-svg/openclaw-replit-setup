# OpenClaw on Replit — Complete Setup

Personal AI assistant via Telegram, powered by Gemini (via Portkey), running 24/7 on Replit.

## What This Is
- **OpenClaw** gateway running 24/7 on Replit
- **Telegram bot** connected (responds only to your chat ID)
- **Model**: Gemini 3.5 Flash via Portkey proxy
- **No public UI** — headless/private mode
- **Status page** available for deploy health checks

## Architecture
```
You (Telegram) → OpenClaw Gateway → Portkey → Google Gemini
```

## Quick Start on a New Replit

### 1. Import this repo into Replit
Create a new Replit, choose "Import from GitHub", paste this repo URL.

### 2. Set these secrets in Replit Secrets tab
| Secret | Value |
|--------|-------|
| `PORTKEY_API_KEY` | Your Portkey API key |
| `PORTKEY_CONFIG` | Your Portkey config ID (e.g. pc-gemini-85dd0b) |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather |

### 3. Install & run
```bash
bash scripts/install.sh
```

### 4. Approve your Telegram chat ID (first time only)
Send any message to your bot. It will reply with a pairing code. Then run:
```bash
export PNPM_HOME="/home/runner/.local/share/pnpm" && export PATH="$PNPM_HOME:$PATH"
openclaw pairing approve telegram <PAIRING_CODE>
```

## Replit Workflow (auto-configured)
```
export PNPM_HOME="/home/runner/.local/share/pnpm" && export PATH="$PNPM_HOME:$PATH" && openclaw gateway run --force --allow-unconfigured
```

## Files
| File | Purpose |
|------|---------|
| `openclaw.json.template` | Config template (copy to `~/.openclaw/openclaw.json`) |
| `SOUL.md` | Agent personality — edit to customize behavior |
| `REPLIT_ENVIRONMENT.md` | Full Replit environment docs for the agent |
| `scripts/install.sh` | One-shot install + setup script |
| `start.sh` | Start script used by Replit workflow |

## Key Notes
- **Telegram pairing**: First time you message the bot, run `openclaw pairing approve telegram <CODE>`. After approval, it works permanently.
- **Model config**: Portkey config ID (`pc-gemini-85dd0b`) routes to Gemini 3.5 Flash.
- **Environment**: Uses `agents.defaults` (plural) not `agents.default` in config.
- **Gateway command**: `openclaw gateway run` not `openclaw gateway:start`.
