# Replit Environment — Complete Reference for OpenClaw

## Overview
This OpenClaw instance runs inside a **Replit** cloud development environment.
Replit is a browser-based IDE and cloud hosting platform. The environment is Ubuntu 24.04 LTS (Noble Numbat) running on top of a NixOS-managed container.

---

## System Details

### OS & Distribution
- **OS**: Ubuntu 24.04.2 LTS (Noble Numbat)
- **Kernel**: Linux (NixOS-managed Nix store at `/nix/store/`)
- **Architecture**: x86_64
- **Home directory**: `/home/runner`
- **Workspace root**: `/home/runner/workspace`

### Runtime Versions
- **Node.js**: v24.13.0 (recommended; v22.19+ minimum)
- **npm**: 10.26.1
- **pnpm**: 10.26.1
- **Python**: 3.x (available via `python3`)
- **pip**: available via `pip3`
- **Bun**: may be available (check with `bun --version`)

---

## Package Management

### How Replit Manages Packages

Replit uses a **dual package management system**:

#### 1. Nix (System/Language Packages)
- Configuration file: `/home/runner/workspace/replit.nix` or `.replit` config
- Used for: system packages, language runtimes, tools
- Nix store: `/nix/store/`
- To add a Nix package: edit `replit.nix` and add to `deps = [...]`
- Example: `pkgs.python311`, `pkgs.nodejs_20`, `pkgs.git`
- Nix packages are **declarative** — edit the config file, Replit applies it

#### 2. npm/pnpm (Node.js packages)
- This project uses **pnpm** as the primary package manager
- Workspace file: `/home/runner/workspace/pnpm-workspace.yaml`
- Install packages: `pnpm add <package>` (in a workspace package)
- Install globally: `pnpm add -g <package>` (requires PNPM_HOME set)
- Global pnpm bin: `/home/runner/.local/share/pnpm/`

#### 3. pip (Python packages)
- Install: `pip3 install <package>`
- No virtual environments needed — packages install globally

### Installing Global npm/pnpm Packages
```bash
export PNPM_HOME="/home/runner/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
pnpm add -g <package>
```

### PATH in Replit
The PATH includes:
- `/home/runner/.local/share/pnpm` (global pnpm bins)
- `/nix/store/...` (Nix-managed binaries)
- Standard Linux paths

---

## Directory Structure

```
/home/runner/
├── workspace/                  ← Main project root (git repo)
│   ├── .replit                 ← Replit config (workflows, run commands)
│   ├── replit.nix              ← Nix package dependencies
│   ├── pnpm-workspace.yaml     ← pnpm monorepo workspace config
│   ├── package.json            ← Root package.json
│   ├── artifacts/              ← Replit artifacts (web apps, APIs)
│   │   ├── api-server/         ← Express API server artifact
│   │   └── mockup-sandbox/     ← React mockup sandbox
│   └── .agents/                ← Agent memory and skills
│       └── memory/
├── .openclaw/                  ← OpenClaw config directory
│   ├── openclaw.json           ← Main OpenClaw configuration
│   ├── SOUL.md                 ← Agent personality/rules
│   └── REPLIT_ENVIRONMENT.md   ← This file
└── .local/
    └── share/pnpm/             ← Global pnpm packages
        └── openclaw            ← OpenClaw binary
```

---

## Replit Workflows

Replit uses **workflows** (defined in `.replit`) to manage long-running processes:
- Workflows are like systemd services — they auto-start and restart
- Configured in `.replit` file under `[workflows]` section
- The OpenClaw gateway runs as a Replit workflow

### OpenClaw Workflow Command
```bash
export PNPM_HOME="/home/runner/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
openclaw gateway:start --no-ui
```

---

## Environment Variables & Secrets

Replit stores secrets as environment variables, accessible at runtime:
- `PORTKEY_API_KEY` — Portkey gateway API key
- `PORTKEY_CONFIG` — Portkey config ID (e.g., pc-gemini-85dd0b)
- `TELEGRAM_BOT_TOKEN` — Telegram bot token
- `TELEGRAM_CHAT_ID` — Allowed Telegram chat ID
- `OPENCLAW_MODEL` — Default model (e.g., gemini-3.5-flash)
- `PORTKEY_BASE_URL` — https://api.portkey.ai/v1
- `GITHUB_PERSONAL_ACCESS_TOKEN` — GitHub PAT for repo operations

---

## Networking

- **Replit proxy**: Apps are served through a reverse proxy at `https://<repl-name>.<user>.repl.co`
- **Internal ports**: Apps bind to `process.env.PORT` (assigned by Replit)
- **Localhost**: `127.0.0.1` is accessible internally
- **External access**: Only ports exposed via Replit proxy are public
- **No Docker**: Replit does not support Docker containers
- **No sudo**: Limited sudo access; use Nix for system packages

---

## File System Notes

- **Persistent storage**: `/home/runner/workspace/` is persistent (git-tracked)
- **OpenClaw config**: `/home/runner/.openclaw/` is persistent
- **Temp files**: `/tmp/` is available but not persistent across restarts
- **Git**: The workspace is a git repository

---

## Replit-Specific Features

### Secrets Management
- Secrets are managed via Replit's UI (Secrets tab)
- Accessed as normal environment variables: `process.env.SECRET_NAME`
- Never commit secrets to git — use env vars

### Database
- Replit provides PostgreSQL via `DATABASE_URL` environment variable
- Also provides key-value store via `@replit/database`

### Object Storage
- Available via Replit's App Storage (S3-compatible)

---

## OpenClaw Installation on Replit

### Initial Setup (Already Done)
```bash
export PNPM_HOME="/home/runner/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
pnpm add -g openclaw@latest
# Config files placed in ~/.openclaw/
```

### Starting OpenClaw
```bash
export PNPM_HOME="/home/runner/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
openclaw gateway:start --no-ui
```

### Updating OpenClaw
```bash
export PNPM_HOME="/home/runner/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"
pnpm add -g openclaw@latest
```

### Checking Status
```bash
openclaw doctor
openclaw status
```

---

## LiteLLM / Portkey Proxy Configuration

This instance uses **Portkey** as the LLM gateway (no separate LiteLLM needed).
Portkey is configured in `openclaw.json` under `models.providers.portkey`.

The Portkey endpoint is OpenAI-compatible:
- Base URL: `https://api.portkey.ai/v1`
- Auth: `x-portkey-api-key` header
- Config: `x-portkey-config` header (selects the routing config)

Model requests go: OpenClaw → Portkey API → Google Gemini

---

## Telegram Bot Setup

The bot is configured in `openclaw.json` under `channels.telegram`.
- Uses grammY framework internally
- Token from `TELEGRAM_BOT_TOKEN` env var
- Only accepts messages from allowlisted chat IDs
- No public webhook URL needed (uses long-polling by default in dev)
- For production: set `webhook.url` in config

---

## Troubleshooting on Replit

| Issue | Solution |
|-------|---------|
| `openclaw: command not found` | `export PNPM_HOME="/home/runner/.local/share/pnpm"; export PATH="$PNPM_HOME:$PATH"` |
| Port already in use | Change gateway port in openclaw.json or kill process |
| Can't install packages | Use `pnpm add -g` with PNPM_HOME set |
| Nix package needed | Edit `replit.nix`, add to deps array |
| Workflow not starting | Check `.replit` workflows config |
| Secrets not loading | Verify secret names in Replit Secrets tab |
