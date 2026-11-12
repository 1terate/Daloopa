"""Shared DeepSeek client (OpenAI-compatible) + helpers."""
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
MODEL = "deepseek-chat"


def chat(prompt: str, system: str = "You are a precise financial data assistant.", **kw) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=kw.pop("temperature", 0),
        **kw,
    )
    return r.choices[0].message.content


def chat_json(prompt: str, system: str = "Reply with a single JSON object only.") -> dict:
    """JSON mode: the prompt must mention 'json' and describe the shape you want."""
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(r.choices[0].message.content)
