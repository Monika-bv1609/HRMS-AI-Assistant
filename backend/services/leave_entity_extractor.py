import json

from services.llm_service import client


def extract_leave_entity(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": """
You are a JSON extractor.

Extract employee_name from the question.

Return ONLY valid JSON.

Examples:

Question:
Is Mitchell Admin on leave today?

Output:
{
    "employee_name": "Mitchell Admin"
}

Question:
Is he on leave today?

Output:
{
    "employee_name": null
}

Rules:
- Return ONLY JSON
- No explanation
- No markdown
- No sentences
- No code block
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
        f"LEAVE ENTITY RAW: {result}"
    )

    try:

        entity = json.loads(
            result
        )

        print(
            f"LEAVE ENTITY PARSED: {entity}"
        )

        return entity

    except Exception as e:

        print(
            f"LEAVE ENTITY ERROR: {e}"
        )

        return {

            "employee_name": None
        }