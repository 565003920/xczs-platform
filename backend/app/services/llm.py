"""
LLM enhancement service.
Supports DeepSeek and Tongyi (通义千问).
When no API key is configured, falls back to None (caller uses rule-based logic).
"""
import os
import time
import logging
import httpx
from typing import Optional

logger = logging.getLogger("xczs.llm")

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
    start = time.time()

    logger.info("=" * 60)
    logger.info(f"[LLM] → REQUEST: {cfg['model']} | max_tokens={max_tokens}")
    logger.info(f"[LLM] → SYSTEM: {system_prompt}")
    logger.info(f"[LLM] → USER:   {user_prompt}")

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
        elapsed = time.time() - start

        if resp.status_code != 200:
            logger.error(f"[LLM] ← ERROR {resp.status_code} in {elapsed:.1f}s: {resp.text[:500]}")
            logger.info("=" * 60)
            return None

        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        tokens_used = data.get("usage", {}).get("total_tokens", "?")

        logger.info(f"[LLM] ← RESPONSE: {elapsed:.1f}s | {tokens_used} tokens | {len(content)} chars")
        logger.info(f"[LLM] ← CONTENT: {content}")
        logger.info("=" * 60)

        return content
    except Exception as e:
        elapsed = time.time() - start
        logger.error(f"[LLM] ← Request failed ({elapsed:.1f}s): {e}")
        return None
