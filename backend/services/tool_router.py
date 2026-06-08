import json

from services.llm_service import client


def select_tool(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": """
You are an HR tool router.

Available tools:

employee_search
leave_status
leave_policy
leave_application

Return ONLY valid JSON.

Examples:

User:
Who is Rachel Perry?

Output:
{
    "tool": "employee_search",
    "employee_name": "Rachel Perry"
}

User:
Rachel's email

Output:
{
    "tool": "employee_search",
    "employee_name": "Rachel",
    "request_type": "email"
}

User:
Is Rachel on leave today?

Output:
{
    "tool": "leave_status",
    "employee_name": "Rachel"
}

User:
Apply leave for me tomorrow

Output:
{
    "tool": "leave_application"
}

User:
What leave types are available?

Output:
{
    "tool": "leave_policy"
}

Return only JSON.
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

    return json.loads(result)