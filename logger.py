"""Append-only JSONL log of every interaction (for debugging + scorecards)."""
import json
import time
from pathlib import Path

LOG = Path(__file__).parent / "logs" / "interactions.jsonl"


def log(**fields):
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps({"ts": time.time(), **fields}, default=str) + "\n")


def read_logs() -> list[dict]:
    return [json.loads(l) for l in LOG.open()] if LOG.exists() else []
