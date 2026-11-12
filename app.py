"""Streamlit shell. Run: .venv/bin/streamlit run app.py"""
import pandas as pd
import streamlit as st

from extract import extract, pdf_text

st.set_page_config(page_title="Filing Extractor", layout="wide")
st.title("Filing Extractor")

up = st.file_uploader("Upload a filing (PDF)", type="pdf")
raw = st.text_area("...or paste filing text", height=150)
metrics = st.text_input("Metrics (comma-separated)", "Total revenue, Net income, Diluted EPS")

if st.button("Extract") and (up or raw):
    text = pdf_text(up) if up else raw
    with st.spinner("Extracting..."):
        rows = extract(text, [m.strip() for m in metrics.split(",") if m.strip()])
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
