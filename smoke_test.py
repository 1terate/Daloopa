"""Run before the round: .venv/bin/python smoke_test.py"""
import socket
import sys

print("python", sys.version.split()[0])
from llm import chat  # noqa: E402

print("deepseek:", chat("Reply with exactly: READY"))
s = socket.socket()
print("port 8501:", "free" if s.connect_ex(("127.0.0.1", 8501)) else "IN USE")
