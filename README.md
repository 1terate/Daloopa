# Interview starter

Generic plumbing only — the real logic gets built live.

## Before the round
```
cd ~/daloopa-interview && source .venv/bin/activate
python smoke_test.py
```

## Files
| File | What it is |
|---|---|
| `llm.py` | DeepSeek client: `chat()`, `chat_json()`, `timed()`. Key from `.env` or `st.secrets` |
| `agent.py` | Tool-calling loop — add a function + schema to `TOOLS` |
| `loaders.py` | PDF text/tables, CSV/Excel, URL fetch |
| `logger.py` | JSONL interaction log |
| `app.py` | Streamlit shell (Run + Logs tabs). Replace `process()` |
| `evals/run_eval.py` | Golden-set runner: fill `CASES`, `PREDICT`, `SCORE` |
| `smoke_test.py` | Python / key / JSON mode / port check |

## Run
```
streamlit run app.py          # localhost:8501
python agent.py
python -m evals.run_eval
```

## Deploy (Streamlit Community Cloud)
share.streamlit.io → New app → this repo, `app.py`, Python 3.11 → Advanced → Secrets:
`DEEPSEEK_API_KEY = "sk-..."`

## Never commit
`.env`, `.streamlit/secrets.toml` (both in `.gitignore`).
