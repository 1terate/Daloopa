"""Run right before the round: python smoke_test.py"""
import socket
import sys

ok = sys.version_info >= (3, 10)
print("python", sys.version.split()[0], "OK" if ok else "TOO OLD - use .venv")
from llm import chat, chat_json  # noqa: E402

print("deepseek chat:", chat("Reply with exactly: READY"))
print("deepseek json:", chat_json('Return {"status": "ok"}'))
s = socket.socket()
print("port 8501:", "free" if s.connect_ex(("127.0.0.1", 8501)) else "IN USE (streamlit run app.py --server.port 8502)")
