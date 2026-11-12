"""
Minimal agent-builder harness: DeepSeek (OpenAI-compatible API) + tool use.

Extend this live during the interview:
  - add more tools to TOOLS + TOOL_IMPLS below
  - swap the example tool for whatever the exercise needs
  - the loop below is a standard manual tool-calling agentic loop
"""
import json
import os

from llm import MODEL, client



def get_example_data(query: str) -> str:
    """Replace with a real tool implementation."""
    return f"No real data source wired up yet for: {query}"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_example_data",
            "description": "Look up example data for a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to look up."},
                },
                "required": ["query"],
            },
        },
    },
]

TOOL_IMPLS = {"get_example_data": get_example_data}


def run(user_message: str):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )
        choice = response.choices[0]
        messages.append(choice.message)

        if choice.finish_reason != "tool_calls":
            print(choice.message.content)
            return

        for tool_call in choice.message.tool_calls:
            fn = TOOL_IMPLS[tool_call.function.name]
            args = json.loads(tool_call.function.arguments)
            result = fn(**args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )


if __name__ == "__main__":
    run("Say hello and tell me you're ready to build.")
