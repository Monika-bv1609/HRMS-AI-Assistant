import json

from services.llm_service import client


def select_tool(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": """
You are a classifier.

Choose ONLY ONE value from:

employee_search
leave_status
leave_policy
apply_leave

Examples:

Who is Rachel Perry?
employee_search

Rachel's email
employee_search

Is Rachel on leave today?
leave_status

Who is on leave today?
leave_status

What leave types are available?
leave_policy

Apply leave for me tomorrow
apply_leave

Rules:
- Return only the tool name.
- Do not answer the question.
- Do not explain.
- Do not use JSON.
- Output must be one word from the list above.
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
        f"TOOL ROUTER RAW: {result}"
    )

    return result