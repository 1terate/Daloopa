"""DeepSeek client (OpenAI-compatible). Key from .env locally, st.secrets when hosted."""
import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _key() -> str:
    """Key from env/.env first, then Streamlit secrets (top level or inside any [section])."""
    key = os.getenv("DEEPSEEK_API_KEY")
    if key:
        return key.strip()
    seen = []
    try:
        import streamlit as st
        secrets = dict(st.secrets)
        seen = list(secrets)
        for name, val in secrets.items():
            if name.upper() == "DEEPSEEK_API_KEY":
                return str(val).strip()
            if hasattr(val, "items"):
                for sub, v in val.items():
                    if sub.upper() == "DEEPSEEK_API_KEY":
                        return str(v).strip()
    except Exception:
        pass
    raise RuntimeError(
        "DEEPSEEK_API_KEY not found. Locally: add it to .env. "
        'Streamlit Cloud: Settings > Secrets > DEEPSEEK_API_KEY = "sk-..." then Reboot app. '
        f"Secret names Streamlit can see: {seen or 'none'}"
    )


client = OpenAI(api_key=_key(), base_url="https://api.deepseek.com")
MODEL = "deepseek-chat"
DEFAULT_SYSTEM = "You are a precise assistant. If you are not sure, say so instead of guessing."


def chat(prompt: str, system: str = DEFAULT_SYSTEM, temperature: float = 0) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return r.choices[0].message.content


def chat_json(prompt: str, system: str = "Reply with a single JSON object only.") -> dict:
    """JSON mode. Describe the exact JSON shape you want in the prompt."""
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt + "\n\nRespond in json."}],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(r.choices[0].message.content)


def timed(fn, *args, **kw):
    """Returns (result, latency_ms) - handy for a scorecard."""
    t = time.perf_counter()
    out = fn(*args, **kw)
    return out, round((time.perf_counter() - t) * 1000)
