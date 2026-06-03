from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def classify_intent(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",
                "content": """
            You are an intent classifier.

            Return ONLY one of:

            employee_count
            employee_search
            leave_today
            leave_count
            leave_status
            leave_policy
            leave_application

            Examples:

            How many employees are there?
            -> employee_count

            Find employee Mitchell
            -> employee_search

            Who is on leave today?
            -> leave_today

            How many employees are on leave today?
            -> leave_count

            Is Mitchell on leave today?
            -> leave_status

            Is he on leave today?
            -> leave_status

            Rules:
            - Return only the intent
            - No explanation
            - No JSON
            - No code
            """
            },

            {
                "role": "user",
                "content": question
            }

        ],

        temperature=0
    )

    intent = (

        response
        .choices[0]
        .message
        .content
        .strip()
        .lower()
    )

    print(
        f"RAW LLM RESPONSE: [{intent}]"
    )

    if "employee_search" in intent:
        return "employee_search"

    if "employee_count" in intent:
        return "employee_count"

    if "leave_today" in intent:
        return "leave_today"

    if "leave_count" in intent:
        return "leave_count"

    if "leave_status" in intent:
        return "leave_status"
    
    if "leave_policy" in intent:
        return "leave_policy"
    
    if "leave_application" in intent:
        return "leave_application"

    return "unknown"