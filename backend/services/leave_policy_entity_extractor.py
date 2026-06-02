import json

from services.llm_service import client


def extract_leave_policy_entity(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": """
You are a JSON extractor.

Extract:

1. leave_type

Return ONLY valid JSON.

Examples:

{
    "leave_type": "Sick Time Off"
}

{
    "leave_type": "Paid Time Off"
}

{
    "leave_type": null
}

Rules:
- Return only JSON
- No explanation
- No markdown
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
        f"LEAVE POLICY ENTITY RAW: {result}"
    )

    try:

        return json.loads(result)

    except:

        return {

            "leave_type": None
        }