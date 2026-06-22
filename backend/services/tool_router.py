import json
from pathlib import Path

from langsmith import traceable

from services.llm_service import client


PROMPT_VERSION = "v1"

SYSTEM_PROMPT = Path(
    f"prompts/tool_router_{PROMPT_VERSION}.txt"
).read_text(encoding="utf-8")


@traceable(
    name="tool_router",
    metadata={
        "prompt_version": PROMPT_VERSION
    }
)
def select_tool(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": question
            }

        ],

        temperature=0
    )

    result = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    print(f"TOOL ROUTER RAW: {result}")

    try:
        return json.loads(result)

    except Exception as e:

        print(f"TOOL ROUTER JSON ERROR: {e}")

        return {
            "tool": "unknown"
        }