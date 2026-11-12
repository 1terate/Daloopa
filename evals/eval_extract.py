"""Golden-set eval for extract(). Run: .venv/bin/python -m evals.eval_extract
Score value accuracy and verification separately; a null is correct when the metric isn't in the text."""
from extract import extract

CASES = [
    {"text": "Total revenue was $94.9 billion, up 6%.", "metric": "Total revenue", "expected": 94.9},
    {"text": "Revenue rose 6% to $94.9B; net income fell to $14.7B.", "metric": "Net income", "expected": 14.7},
    {"text": "Revenue grew 6% year over year.", "metric": "Total revenue", "expected": None},  # % is a trap, not revenue
    {"text": "Diluted EPS was $1.64 vs $1.46 a year ago.", "metric": "Diluted EPS", "expected": 1.64},  # prior-period trap
]

if __name__ == "__main__":
    ok = 0
    for c in CASES:
        m = extract(c["text"], [c["metric"]])[0]
        hit = m["value"] == c["expected"] or (m["value"] is not None and c["expected"] is not None and abs(m["value"] - c["expected"]) < 1e-6)
        ok += hit
        print(("PASS" if hit else "FAIL"), c["metric"], "->", m["value"], "| verified:", m["verified"])
    print(f"\n{ok}/{len(CASES)} correct")
