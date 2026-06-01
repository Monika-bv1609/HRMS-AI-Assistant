from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def classify_intent(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",
                "content": """
You are an intent classifier.

Return ONLY one of these exact values:

employee_count
leave_today
employee_search

Rules:
- Never explain
- Never generate code
- Never generate examples
- Never generate sentences
- Return only the intent value
"""
            },

            {
                "role": "user",
                "content": question
            }

        ],

        temperature=0
    )

    intent = (

        response
        .choices[0]
        .message
        .content
        .strip()
        .lower()
    )

    print(f"RAW LLM RESPONSE: [{intent}]")

    if "employee_search" in intent:
        return "employee_search"

    if "employee_count" in intent:
        return "employee_count"

    if "leave_today" in intent:
        return "leave_today"

    return "unknown"