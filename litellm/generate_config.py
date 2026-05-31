#!/usr/bin/env python3
"""
Generate LiteLLM config.yaml for gemini-3.5-flash round-robin.
Only loads keys that pass Google's validation (not leaked/revoked).

VALID keys (tested 2026-05-31): GOOGLE_API_KEY1, GOOGLE_API_KEY3, GOOGLE_API_KEY9
LEAKED keys (reported by Google, do NOT use):
  GOOGLE_API_KEY2,4,5,6,7,8,10,111,12,13,14,16,GOOGLE_API_KEY
"""
import os
import yaml

# Only include keys confirmed valid — update this list after replacing leaked keys
VALID_KEY_NAMES = [
    "GOOGLE_API_KEY1",
    "GOOGLE_API_KEY3",
    "GOOGLE_API_KEY9",
]

model_list = []
for name in VALID_KEY_NAMES:
    key = os.environ.get(name, "").strip()
    if key:
        model_list.append({
            "model_name": "gemini-3.5-flash",
            "litellm_params": {
                "model": "gemini/gemini-3.5-flash",
                "api_key": key,
            }
        })

if not model_list:
    print("ERROR: No valid GOOGLE_API_KEY* secrets found!")
    exit(1)

print(f"[LiteLLM] Loaded {len(model_list)} valid API keys for round-robin")

config = {
    "model_list": model_list,
    "router_settings": {
        "routing_strategy": "simple-shuffle",
        "num_retries": len(model_list) * 2,
        "retry_after": 1,
        "allowed_fails": 1,
        "cooldown_time": 60,
        "retry_policy": {
            "AuthenticationErrorRetryPolicy": {
                "num_retries": len(model_list),
                "retry_after": 0,
            },
            "RateLimitErrorRetryPolicy": {
                "num_retries": len(model_list) * 2,
                "retry_after": 2,
            },
        },
    },
    "litellm_settings": {
        "drop_params": True,
        "request_timeout": 120,
        "telemetry": False,
    },
    "general_settings": {
        "master_key": "sk-litellm-local",
        "disable_spend_logs": True,
    }
}

out = "/tmp/litellm_config.yaml"
with open(out, "w") as f:
    yaml.dump(config, f, default_flow_style=False)

print(f"[LiteLLM] Config written to {out} ({len(model_list)} keys)")
