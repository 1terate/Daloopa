# Daloopa interview workspace

```
cd ~/daloopa-interview && source .venv/bin/activate
python smoke_test.py          # key + python + port check
python extract.py             # sample extraction with source quotes
python -m evals.eval_extract  # golden-set eval
streamlit run app.py          # UI on :8501
```

- `llm.py` – DeepSeek client, `chat()` and `chat_json()`
- `agent_starter.py` – tool-calling loop
- `extract.py` – numbers + source quote + verify step
- `edgar.py` – SEC EDGAR / XBRL ground truth (set EDGAR_USER_AGENT)
- Python 3.11 venv; `.env` is gitignored
