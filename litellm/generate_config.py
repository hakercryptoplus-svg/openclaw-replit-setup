#!/usr/bin/env python3
"""
Generate LiteLLM config.yaml for gemini-2.0-flash round-robin.
Uses Google AI Studio OpenAI-compatible endpoint (not Vertex AI).
"""
import os
import yaml

KEY_NAMES = [
    "GOOGLE_API_KEY1",
    "GOOGLE_API_KEY2",
    "GOOGLE_API_KEY3",
    "GOOGLE_API_KEY4",
    "GOOGLE_API_KEY5",
    "GOOGLE_API_KEY6",
    "GOOGLE_API_KEY7",
    "GOOGLE_API_KEY8",
    "GOOGLE_API_KEY9",
    "GOOGLE_API_KEY10",
]

GOOGLE_AI_STUDIO_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"

model_list = []
for name in KEY_NAMES:
    key = os.environ.get(name, "").strip()
    if key:
        model_list.append({
            "model_name": "gemini-2.0-flash",
            "litellm_params": {
                "model": "openai/gemini-2.0-flash",
                "api_key": key,
                "api_base": GOOGLE_AI_STUDIO_BASE,
            }
        })

if not model_list:
    print("ERROR: No GOOGLE_API_KEY* secrets found!")
    exit(1)

print(f"[LiteLLM] Loaded {len(model_list)} API keys for round-robin (AI Studio mode)")

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
