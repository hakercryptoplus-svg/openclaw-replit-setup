#!/usr/bin/env python3
"""
Generate LiteLLM config.yaml — routes through Portkey (load-balance across 10 Google keys).
Model: gemini-2.5-flash  |  Portkey config: pc-clawdo-3d7b11
"""
import yaml

PORTKEY_API_KEY = "y51moYEhwp742RUoW4cN1kQYtoUg"
PORTKEY_CONFIG  = "pc-clawdo-3d7b11"
PORTKEY_BASE    = "https://api.portkey.ai/v1"

print("[LiteLLM] Configuring Portkey load-balance (10 Google keys) for gemini-2.5-flash")

config = {
    "model_list": [
        {
            "model_name": "gemini-2.5-flash",
            "litellm_params": {
                "model":    "openai/gemini-2.5-flash",
                "api_key":  PORTKEY_API_KEY,
                "api_base": PORTKEY_BASE,
                "extra_headers": {
                    "x-portkey-api-key": PORTKEY_API_KEY,
                    "x-portkey-config":  PORTKEY_CONFIG,
                },
            },
        }
    ],
    "router_settings": {
        "num_retries": 3,
        "retry_after": 1,
    },
    "litellm_settings": {
        "drop_params":      True,
        "request_timeout":  120,
        "telemetry":        False,
    },
    "general_settings": {
        "master_key":         "sk-litellm-local",
        "disable_spend_logs": True,
    },
}

out = "/tmp/litellm_config.yaml"
with open(out, "w") as f:
    yaml.dump(config, f, default_flow_style=False)

print(f"[LiteLLM] Config written to {out} (Portkey → gemini-2.5-flash)")
