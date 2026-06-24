import requests

from utils.config import PDF_AGENT_URL
from langsmith import traceable

@traceable(name="ask_rag")
def ask_rag(question,policy_type=None):

    response = requests.post(
        f"{PDF_AGENT_URL}/ask-pdf",
        params={
            "question": question,
            "policy_type": policy_type
        }
    )

    print(
        f"[RAG REQUEST] Question={question} | PolicyType={policy_type}"
    )

    response.raise_for_status()

    return response.json()