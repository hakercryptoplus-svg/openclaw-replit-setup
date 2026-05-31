#!/usr/bin/env python3
"""
Generate LiteLLM config.yaml with available Google API keys for round-robin load balancing.
Model: gemini/gemini-3.5-flash
Skips GOOGLE_API_KEY16 (reported as leaked by Google).
"""
import os
import yaml

# NOTE: GOOGLE_API_KEY16 was shown in plaintext in chat — Google auto-revoked it.
# Replace it with a fresh key in Replit Secrets, then add it back here.
KEY_NAMES = [
    "GOOGLE_API_KEY1", "GOOGLE_API_KEY2", "GOOGLE_API_KEY3", "GOOGLE_API_KEY4",
    "GOOGLE_API_KEY5", "GOOGLE_API_KEY6", "GOOGLE_API_KEY7", "GOOGLE_API_KEY8",
    "GOOGLE_API_KEY9", "GOOGLE_API_KEY10", "GOOGLE_API_KEY111", "GOOGLE_API_KEY12",
    "GOOGLE_API_KEY13", "GOOGLE_API_KEY14", "GOOGLE_API_KEY",
]

model_list = []
for name in KEY_NAMES:
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
    print("ERROR: No GOOGLE_API_KEY* secrets found!")
    exit(1)

print(f"[LiteLLM] Loaded {len(model_list)} API keys for round-robin")

config = {
    "model_list": model_list,
    "router_settings": {
        "routing_strategy": "simple-shuffle",
        # Retry up to N times — enough to cycle through all keys
        "num_retries": len(model_list),
        "retry_after": 0,
        # After 1 failure, cool down that key and try the next
        "allowed_fails": 1,
        "cooldown_time": 300,
        # Retry on auth errors (403) so leaked/quota keys are skipped
        "retry_policy": {
            "AuthenticationErrorRetryPolicy": {
                "num_retries": len(model_list),
                "retry_after": 0,
            },
            "RateLimitErrorRetryPolicy": {
                "num_retries": len(model_list),
                "retry_after": 1,
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

print(f"[LiteLLM] Config written to {out} ({len(model_list)} keys, retry_policy=auth+ratelimit)")
