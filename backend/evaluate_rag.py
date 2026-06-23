from dotenv import load_dotenv

load_dotenv()

from langsmith import evaluate
import requests

def rag_app(inputs):

    response = requests.post(
        "http://127.0.0.1:8001/ask-pdf",
        params={
            "question": inputs["question"]
        }
    )

    return response.json()


evaluate(
    rag_app,
    data="rag-evaluation-small",
    experiment_prefix="rag-evaluation"
)