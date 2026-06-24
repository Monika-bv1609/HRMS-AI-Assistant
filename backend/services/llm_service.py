from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


from services.llm_service import client

def classify_policy(question):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content": """
You are a classifier.

Return ONLY one word:

leave
travel
insurance
wfh

Examples:

Question: What is maternity leave policy?
Answer: leave

Question: Can I claim travel reimbursement?
Answer: travel

Question: What insurance benefits do I have?
Answer: insurance

Question: Can I work from home?
Answer: wfh

Return ONLY the category.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ],

        temperature=0
    )

    category = (
        response
        .choices[0]
        .message
        .content
        .strip()
        .lower()
    )

    print(f"[POLICY CLASSIFIER] Category = {category}")

    return category