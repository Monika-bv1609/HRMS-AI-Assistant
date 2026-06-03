import json

from services.llm_service import client


def extract_leave_application(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": """
You are a JSON extractor.

Extract:

1. leave_type
2. start_date
3. end_date
4. reason

Today's date is 2026-06-02.

Examples:

Question:
Apply leave tomorrow because I have fever

Output:

{
    "leave_type": "Sick Time Off",
    "start_date": "2026-06-03",
    "end_date": "2026-06-03",
    "reason": "fever"
}

Question:
Apply leave tomorrow for training

Output:

{
    "leave_type": "Training Time Off",
    "start_date": "2026-06-03",
    "end_date": "2026-06-03",
    "reason": "training"
}

Rules:
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

        return json.loads(result)

    except:

        return None