"""
LLM enhancement service.
Supports DeepSeek and Tongyi (通义千问).
When no API key is configured, falls back to None (caller uses rule-based logic).
"""
import os
import httpx
from typing import Optional

PROVIDER_CONFIG = {
    "deepseek": {
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "default_model": "deepseek-chat",
    },
    "tongyi": {
        "api_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "default_model": "qwen-plus",
    },
}


def is_configured() -> bool:
    """Check if LLM is properly configured and ready to use."""
    provider = os.getenv("LLM_PROVIDER", "").lower()
    api_key = os.getenv("LLM_API_KEY", "")
    return bool(api_key and provider in PROVIDER_CONFIG)


def _get_config() -> dict:
    """Get provider config with env overrides (lazy read)."""
    provider = os.getenv("LLM_PROVIDER", "").lower()
    api_key = os.getenv("LLM_API_KEY", "")
    api_url = os.getenv("LLM_API_URL", "")
    model = os.getenv("LLM_MODEL", "")
    base = PROVIDER_CONFIG.get(provider, {})
    return {
        "api_url": api_url or base.get("api_url", ""),
        "model": model or base.get("default_model", ""),
        "api_key": api_key,
    }


def call_llm(system_prompt: str, user_prompt: str, max_tokens: int = 300) -> Optional[str]:
    """
    Call LLM to enhance text. Returns None if not configured or on failure.
    Caller MUST have fallback logic.
    """
    if not is_configured():
        return None

    cfg = _get_config()
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json",
    }
    body = {
        "model": cfg["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }

    try:
        resp = httpx.post(cfg["api_url"], json=body, headers=headers, timeout=30)
        if resp.status_code != 200:
            print(f"[LLM] API error: {resp.status_code} {resp.text[:200]}")
            return None
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[LLM] Request failed: {e}")
        return None
