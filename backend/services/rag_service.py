import requests

from utils.config import PDF_AGENT_URL
from langsmith import traceable

@traceable(name="ask_rag")
def ask_rag(question):

    response = requests.post(
        f"{PDF_AGENT_URL}/ask-pdf",
        params={
            "question": question
        }
    )

    response.raise_for_status()

    return response.json()