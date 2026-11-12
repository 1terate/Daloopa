"""SEC EDGAR helpers (free, no key). Set EDGAR_USER_AGENT in .env first ("Name email")."""
import os

import requests
from dotenv import load_dotenv

load_dotenv()
HEADERS = {"User-Agent": os.environ.get("EDGAR_USER_AGENT") or "interview-prep research"}


def cik_for(ticker: str) -> str:
    data = requests.get("https://www.sec.gov/files/company_tickers.json", headers=HEADERS, timeout=20).json()
    for row in data.values():
        if row["ticker"].upper() == ticker.upper():
            return str(row["cik_str"]).zfill(10)
    raise KeyError(ticker)


def company_facts(ticker: str) -> dict:
    """XBRL facts: a ground-truth source for evals (e.g. us-gaap Revenues)."""
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_for(ticker)}.json"
    return requests.get(url, headers=HEADERS, timeout=30).json()
