from services.llm_service import client


def classify_confirmation(message):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": """
You are a confirmation classifier.

Classify the user's response into one of:

YES
NO
UNKNOWN

Examples:

yes -> YES
sure -> YES
okay -> YES
go ahead -> YES
please proceed -> YES

no -> NO
cancel -> NO
stop -> NO
never mind -> NO

what is my leave balance -> UNKNOWN

Return ONLY:
YES
NO
or
UNKNOWN
"""
            },

            {
                "role": "user",
                "content": message
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
        .upper()
    )

    print(
        f"CONFIRMATION CLASSIFIER: {result}"
    )

    return result