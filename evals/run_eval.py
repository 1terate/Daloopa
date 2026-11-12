"""Generic golden-set eval runner.
Fill CASES with {"input": ..., "expected": ...}; point PREDICT at the function under test.
Run: python -m evals.run_eval"""
import json

from llm import timed


def PREDICT(x):  # replace with the real function under test
    from llm import chat
    return chat(f"Answer with one word. {x}").strip().strip(".").lower()


def SCORE(pred, expected) -> bool:  # replace with exact / numeric tolerance / LLM judge as needed
    return str(pred).lower() == str(expected).lower()


CASES = [
    {"input": "What color is the sky on a clear day?", "expected": "blue", "tag": "happy_path"},
    {"input": "Is 7 a prime number? yes or no", "expected": "yes", "tag": "happy_path"},
]

if __name__ == "__main__":
    results = []
    for c in CASES:
        pred, ms = timed(PREDICT, c["input"])
        ok = SCORE(pred, c["expected"])
        results.append({**c, "pred": pred, "pass": ok, "ms": ms})
        print(("PASS" if ok else "FAIL"), f"[{c.get('tag','')}]", c["input"][:60], "->", pred)
    n = sum(r["pass"] for r in results)
    print(f"\n{n}/{len(results)} passed | avg {sum(r['ms'] for r in results)//len(results)} ms")
    json.dump(results, open("evals/last_results.json", "w"), indent=2, default=str)
