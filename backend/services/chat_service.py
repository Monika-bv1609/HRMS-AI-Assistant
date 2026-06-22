import requests

from utils.config import PDF_AGENT_URL

from langsmith import traceable

@traceable(name="process_question")
def process_question(question: str):

    response = requests.post(
        f"{PDF_AGENT_URL}/ask-pdf",
        params={
            "question": question
        }
    )

    return response.json()