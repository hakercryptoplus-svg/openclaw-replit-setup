#!/bin/bash
set -e
echo "[LiteLLM] Generating config from Google API key secrets..."
python3 /home/runner/workspace/litellm/generate_config.py

echo "[LiteLLM] Starting proxy on port 4000..."
# Unset Replit PostgreSQL vars so LiteLLM doesn't try to use Prisma
exec env -u DATABASE_URL -u PGDATABASE -u PGHOST -u PGPORT -u PGUSER -u PGPASSWORD \
  /home/runner/workspace/.pythonlibs/bin/litellm \
  --config /tmp/litellm_config.yaml \
  --port 4000 \
  --host 0.0.0.0 \
  --num_workers 1
