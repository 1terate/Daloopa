"""Streamlit shell. Run: streamlit run app.py   -> http://localhost:8501
Replace process() with the real pipeline."""
import pandas as pd
import streamlit as st

from llm import chat, timed
from loaders import any_text
from logger import log, read_logs

st.set_page_config(page_title="Demo", layout="wide")


def process(text: str) -> str:
    return chat(text)


st.title("Demo")
tab_run, tab_logs = st.tabs(["Run", "Logs"])

with tab_run:
    up = st.file_uploader("Upload a file (optional)", type=["pdf", "csv", "xlsx", "txt"])
    q = st.text_area("Input", height=120)
    if st.button("Run", type="primary") and (q or up):
        context = any_text(up) if up else ""
        prompt = f"{q}\n\nCONTEXT:\n{context[:60000]}" if context else q
        with st.spinner("Thinking..."):
            try:
                out, ms = timed(process, prompt)
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()
        st.markdown(out)
        st.caption(f"{ms} ms")
        log(input=q, file=getattr(up, "name", None), output=out, latency_ms=ms)

with tab_logs:
    rows = read_logs()
    if rows:
        df = pd.DataFrame(rows)
        st.metric("Runs", len(df))
        st.metric("Avg latency (ms)", int(df["latency_ms"].mean()))
        st.dataframe(df.iloc[::-1], width="stretch")
    else:
        st.info("No runs yet.")
