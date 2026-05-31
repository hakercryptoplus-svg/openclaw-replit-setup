#!/usr/bin/env python3
"""
Generate LiteLLM config.yaml
Routes: LiteLLM → Portkey virtual keys (1-10) → Google Gemini
Each virtual key maps to one Google AI Studio API key.
LiteLLM does automatic fallback when a key hits quota (429).
"""
import yaml

PORTKEY_API_KEY = "y51moYEhwp742RUoW4cN1kQYtoUg"
PORTKEY_BASE    = "https://api.portkey.ai/v1"

# 10 Portkey virtual keys — each maps to a separate Google API key
VIRTUAL_KEYS = [
    "google-key-1-8f8529",
    "google-key-2-38e499",
    "google-key-3-ced468",
    "google-key-4-aad60f",
    "google-key-5-280065",
    "google-key-6-f7ce0b",
    "google-key-7-57ba36",
    "google-key-8-11ef5f",
    "google-key-9-bec2f6",
    "google-key-10-6359a5",
]

print(f"[LiteLLM] Configuring {len(VIRTUAL_KEYS)} Portkey virtual keys with fallback for gemini-3.5-flash")

model_list = []
for i, vk in enumerate(VIRTUAL_KEYS):
    model_list.append({
        "model_name": "gemini-3.5-flash",
        "litellm_params": {
            "model":    "openai/gemini-3.5-flash",
            "api_key":  PORTKEY_API_KEY,
            "api_base": PORTKEY_BASE,
            "extra_headers": {
                "x-portkey-api-key":     PORTKEY_API_KEY,
                "x-portkey-virtual-key": vk,
            },
        },
        "model_info": {"id": f"gemini-key-{i+1}"},
    })

config = {
    "model_list": model_list,
    "router_settings": {
        "num_retries":          3,
        "retry_after":          1,
        "allowed_fails":        1,
        "cooldown_time":        60,
        "routing_strategy":     "usage-based-routing",
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

print(f"[LiteLLM] Config written to {out} — fallback across {len(VIRTUAL_KEYS)} keys")
