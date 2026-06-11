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
    "employee_name": "Rachel Perry",
    "request_type": "details"
}

User:
Rachel's email

Output:
{
    "tool": "employee_search",
    "employee_name": "Rachel Perry",
    "request_type": "email"
}

User:
Rachel's designation

Output:
{
    "tool": "employee_search",
    "employee_name": "Rachel Perry",
    "request_type": "designation"
}

User:
Is Rachel Perry on leave today?

Output:
{
    "tool": "leave_status",
    "employee_name": "Rachel Perry"
}

User:
Is she on leave today?

Output:
{
    "tool": "leave_status",
    "employee_name": "Rachel Perry"
}

User:
Who is on leave today?

Output:
{
    "tool": "leave_status",
    "employee_name": null
}

User:
What leave types are available?

Output:
{
    "tool": "leave_policy"
}

User:
Tell me about Sick Time Off

Output:
{
    "tool": "leave_policy",
    "leave_type": "Sick Time Off"
}

User:
Apply leave for me tomorrow

Output:
{
    "tool": "leave_application",
    "employee_name": null,
    "leave_type": "Sick Time Off",
    "start_date": "tomorrow",
    "end_date": "tomorrow",
    "reason": null
}

User:
Apply sick leave for me tomorrow

Output:
{
    "tool": "leave_application",
    "employee_name": null,
    "leave_type": "Sick Time Off",
    "start_date": "tomorrow",
    "end_date": "tomorrow",
    "reason": null
}

User:
Apply leave for Rachel Perry tomorrow

Output:
{
    "tool": "leave_application",
    "employee_name": "Rachel Perry",
    "leave_type": "Sick Time Off",
    "start_date": "tomorrow",
    "end_date": "tomorrow",
    "reason": null
}

User:
Apply leave for me tomorrow

Output:
{
    "tool": "leave_application",
    "employee_name": null,
    "leave_type": "Sick Time Off",
    "start_date": "tomorrow",
    "end_date": "tomorrow",
    "reason": null
}

User:
Apply sick leave for me tomorrow

Output:
{
    "tool": "leave_application",
    "employee_name": null,
    "leave_type": "Sick Time Off",
    "start_date": "tomorrow",
    "end_date": "tomorrow",
    "reason": null
}

User:
Apply leave for Rachel Perry tomorrow

Output:
{
    "tool": "leave_application",
    "employee_name": "Rachel Perry",
    "leave_type": "Sick Time Off",
    "start_date": "tomorrow",
    "end_date": "tomorrow",
    "reason": null
}

User:
Apply leave for Rachel Perry tomorrow because she is sick

Output:
{
    "tool": "leave_application",
    "employee_name": "Rachel Perry",
    "leave_type": "Sick Time Off",
    "start_date": "tomorrow",
    "end_date": "tomorrow",
    "reason": "sick"
}

User:
What leave types are available?

Output:
{
    "tool": "leave_policy"
}

User:
Tell me about Sick Time Off

Output:
{
    "tool": "leave_policy",
    "leave_type": "Sick Time Off"
}

User:
Explain Casual Leave

Output:
{
    "tool": "leave_policy",
    "leave_type": "Casual Leave"
}

User:
How many employees are there?

Output:
{
    "tool": "employee_search",
    "request_type": "count"
}

User:
What is the employee count?

Output:
{
    "tool": "employee_search",
    "request_type": "count"
}

User:
How many leave requests are there?

Output:
{
    "tool": "leave_status",
    "request_type": "count"
}

User:
What is the total leave count?

Output:
{
    "tool": "leave_status",
    "request_type": "count"
}

User:
Who is on leave today?

Output:
{
    "tool": "leave_status",
    "request_type": "today_list"
}

Rules:

- Return ONLY JSON.
- Never explain.
- Never answer the question.
- No markdown.
- No code blocks.
- No extra text.

- Never generate hardcoded example dates.
- Preserve dates exactly as provided by the user.
- For relative dates return:
  today
  tomorrow
  next Monday
  next week
- For explicit dates return the actual date mentioned by the user.
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

    try:

        return json.loads(
            result
        )

    except Exception as e:

        print(
            f"TOOL ROUTER JSON ERROR: {e}"
        )

        return {

            "tool": "unknown"
        }