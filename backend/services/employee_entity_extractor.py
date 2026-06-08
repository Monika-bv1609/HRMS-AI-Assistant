import json

from services.llm_service import client


def extract_employee_entity(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": """
You are an employee entity extractor.

Your job is ONLY to extract:

1. employee_name
2. request_type

Allowed request_type values:

details
email
designation

IMPORTANT RULES:

- Never answer the user's question.
- Never use your own knowledge.
- Never say:
  - I don't know
  - I don't have information
  - Employee not found
- Never explain anything.
- Return ONLY valid JSON.
- No markdown.
- No code blocks.
- No extra text.

Examples:

User:
Who is Mitchell Admin?

Output:
{
    "employee_name": "Mitchell Admin",
    "request_type": "details"
}

User:
Who is Rachel Perry?

Output:
{
    "employee_name": "Rachel Perry",
    "request_type": "details"
}

User:
Rachel's email

Output:
{
    "employee_name": "Rachel",
    "request_type": "email"
}

User:
Rachel's designation

Output:
{
    "employee_name": "Rachel",
    "request_type": "designation"
}
"""
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

    print(
        f"ENTITY EXTRACTOR RAW: {result}"
    )

    try:

        entity = json.loads(
            result
        )

        print(
            f"ENTITY EXTRACTOR PARSED: {entity}"
        )

        return entity

    except Exception as e:

        print(
            f"JSON PARSE ERROR: {e}"
        )

        print(
            f"RAW RESPONSE: {result}"
        )

        return {

            "employee_name": None,

            "request_type": "details"
        }