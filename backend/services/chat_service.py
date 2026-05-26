import requests

from utils.config import PDF_AGENT_URL


def process_question(question: str):

    response = requests.post(
        f"{PDF_AGENT_URL}/ask-pdf",
        params={
            "question": question
        }
    )

    return response.json()