"""Tool-calling agent loop. Add a function + its schema to TOOLS to give the model a new tool."""
import json

from llm import MODEL, client


def example_tool(query: str) -> str:
    return f"(stub) no data source wired up for: {query}"


TOOLS = {
    example_tool: {
        "description": "Look up data for a query.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
    },
}


def run(user_message: str, system: str = "Use tools when you need data. Never invent numbers.", max_steps: int = 8) -> str:
    impls = {f.__name__: f for f in TOOLS}
    schemas = [{"type": "function", "function": {"name": f.__name__, **s}} for f, s in TOOLS.items()]
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user_message}]
    for _ in range(max_steps):
        choice = client.chat.completions.create(model=MODEL, messages=messages, tools=schemas).choices[0]
        messages.append(choice.message)
        if choice.finish_reason != "tool_calls":
            return choice.message.content
        for tc in choice.message.tool_calls:
            result = impls[tc.function.name](**json.loads(tc.function.arguments))
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
    return "Stopped: too many tool steps."


if __name__ == "__main__":
    print(run("Use the tool to look up 'test', then say you're ready."))
