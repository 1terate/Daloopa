"""DeepSeek client (OpenAI-compatible). Key from .env locally, st.secrets when hosted."""
import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _key() -> str:
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets["DEEPSEEK_API_KEY"]
        except Exception:
            raise RuntimeError("DEEPSEEK_API_KEY not found in .env or Streamlit secrets")
    return key


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
