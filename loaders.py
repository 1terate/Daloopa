"""Turn common inputs into text / tables."""
import io

import pandas as pd


def pdf_text(file, max_pages: int = 50) -> str:
    import pdfplumber
    with pdfplumber.open(file) as pdf:
        return "\n".join(f"[page {i+1}]\n{p.extract_text() or ''}" for i, p in enumerate(pdf.pages[:max_pages]))


def pdf_tables(file, max_pages: int = 50) -> list[pd.DataFrame]:
    import pdfplumber
    out = []
    with pdfplumber.open(file) as pdf:
        for p in pdf.pages[:max_pages]:
            out += [pd.DataFrame(t[1:], columns=t[0]) for t in p.extract_tables() if t and len(t) > 1]
    return out


def table(file, name: str = "") -> pd.DataFrame:
    name = name or getattr(file, "name", "")
    return pd.read_excel(file) if name.endswith((".xlsx", ".xls")) else pd.read_csv(file)


def any_text(file) -> str:
    name = getattr(file, "name", str(file))
    if name.endswith(".pdf"):
        return pdf_text(file)
    if name.endswith((".csv", ".xlsx", ".xls")):
        return table(file, name).to_csv(index=False)
    data = file.read() if hasattr(file, "read") else open(file, "rb").read()
    return data.decode("utf-8", errors="ignore") if isinstance(data, bytes) else data


def url_text(url: str) -> str:
    import requests
    r = requests.get(url, headers={"User-Agent": "research-script"}, timeout=20)
    r.raise_for_status()
    return r.text
