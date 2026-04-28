import os
from anthropic import Anthropic
from app.prompts import SYSTEM_PROMPT

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def chat(messages: list) -> str:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=messages
    )
    result = ""
    for block in response.content:
        if block.type == "text":
            result += block.text
    return result
