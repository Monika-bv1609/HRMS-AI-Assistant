import json

from services.llm_service import client


def extract_employee_entity(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": """
You are a JSON extractor.

Extract:

1. employee_name
2. request_type

Allowed request_type values:

details
email
designation

Rules:

- Return ONLY valid JSON
- No explanation
- No markdown
- No code block
- No extra text
- No sentences

Examples:

{
    "employee_name": "Mitchell Admin",
    "request_type": "details"
}

{
    "employee_name": "Mitchell Admin",
    "request_type": "email"
}

{
    "employee_name": "Mitchell Admin",
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

        return {

            "employee_name": None,

            "request_type": "details"
        }