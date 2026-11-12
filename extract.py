"""Example slice: pull financial figures from filing text WITH source quotes.

Rule: every number must come with the exact sentence it came from; if not found -> null.
Then verify the number actually appears in that quote (don't trust the model).
"""
import re

import pdfplumber

from llm import chat_json

PROMPT = """From the filing text below, extract these metrics as json:
{{"metrics": [{{"name": str, "value": number|null, "unit": str, "period": str, "source_quote": str}}]}}
Metrics: {metrics}
Only use numbers that appear verbatim in the text. If a metric is not present, value=null and source_quote="".

TEXT:
{text}"""


def pdf_text(path: str, max_pages: int = 20) -> str:
    with pdfplumber.open(path) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages[:max_pages])


def _digits(s: str) -> str:
    return re.sub(r"[^\d.]", "", s)


def verify(m: dict, text: str) -> bool:
    """Number must appear in the quote, and the quote must appear in the source text."""
    if m.get("value") is None:
        return True
    q = m.get("source_quote", "")
    v = _digits(str(m["value"])).rstrip("0").rstrip(".")
    return bool(q) and q[:60] in text and v in _digits(q)


def extract(text: str, metrics: list[str]) -> list[dict]:
    out = chat_json(PROMPT.format(metrics=", ".join(metrics), text=text[:60000]))["metrics"]
    for m in out:
        m["verified"] = verify(m, text)
    return out


if __name__ == "__main__":
    sample = "Total revenue was $94.9 billion for the quarter, up 6% year over year. Net income was $14.7 billion."
    for row in extract(sample, ["Total revenue", "Net income", "Operating cash flow"]):
        print(row)
