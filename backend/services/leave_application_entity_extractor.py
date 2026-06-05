import json

from datetime import (
    date,
    timedelta
)

from services.llm_service import client


def extract_leave_application(
    question
):

    today = date.today()

    tomorrow = (
        today
        + timedelta(days=1)
    )

    response = (
        client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",

                    "content": f"""
You are a JSON extractor.

Today's date is {today}.

Extract:

1. employee_name
2. leave_type
3. start_date
4. end_date
5. reason

Return ONLY valid JSON.

Examples:

Question:
Apply leave tomorrow because I have fever

Output:

{{
    "employee_name": null,
    "leave_type": "Sick Time Off",
    "start_date": "{tomorrow}",
    "end_date": "{tomorrow}",
    "reason": "fever"
}}

Question:
Apply leave for Rachel Perry tomorrow because she is sick

Output:

{{
    "employee_name": "Rachel Perry",
    "leave_type": "Sick Time Off",
    "start_date": "{tomorrow}",
    "end_date": "{tomorrow}",
    "reason": "sick"
}}

Question:
Create Sick Time Off for Mitchell Admin tomorrow

Output:

{{
    "employee_name": "Mitchell Admin",
    "leave_type": "Sick Time Off",
    "start_date": "{tomorrow}",
    "end_date": "{tomorrow}",
    "reason": null
}}

Question:
Create Paid Time Off for Rachel Perry from 2026-06-10 to 2026-06-15

Output:

{{
    "employee_name": "Rachel Perry",
    "leave_type": "Paid Time Off",
    "start_date": "2026-06-10",
    "end_date": "2026-06-15",
    "reason": null
}}

Rules:

- Use today's date as reference
- Convert relative dates like tomorrow, next week, next Monday into actual dates
- Return ONLY JSON
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
    )

    result = (

        response
        .choices[0]
        .message
        .content
        .strip()
    )

    print(
        f"LEAVE APPLICATION RAW: {result}"
    )

    try:

        return json.loads(
            result
        )

    except Exception as e:

        print(
            f"JSON ERROR: {e}"
        )

        return None