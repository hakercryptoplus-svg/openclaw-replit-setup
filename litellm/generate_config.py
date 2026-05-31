#!/usr/bin/env python3
"""
Generate LiteLLM config.yaml with all available Google API keys for round-robin load balancing.
Model: gemini/gemini-3.5-flash (newest Gemini 3.5 Flash via Google AI API)
"""
import os
import yaml

KEY_NAMES = [
    "GOOGLE_API_KEY1","GOOGLE_API_KEY2","GOOGLE_API_KEY3","GOOGLE_API_KEY4",
    "GOOGLE_API_KEY5","GOOGLE_API_KEY6","GOOGLE_API_KEY7","GOOGLE_API_KEY8",
    "GOOGLE_API_KEY9","GOOGLE_API_KEY10","GOOGLE_API_KEY111","GOOGLE_API_KEY12",
    "GOOGLE_API_KEY13","GOOGLE_API_KEY14","GOOGLE_API_KEY16","GOOGLE_API_KEY",
]

model_list = []
for name in KEY_NAMES:
    key = os.environ.get(name, "")
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
        "num_retries": 3,
        "retry_after": 5,
        "allowed_fails": 3,
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

print(f"[LiteLLM] Config written to {out}")
