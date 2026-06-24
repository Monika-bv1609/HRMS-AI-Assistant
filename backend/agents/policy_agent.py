from services.rag_service import (
    ask_rag
)
from services.policy_classifier import (
    classify_policy
)

from langsmith import traceable

@traceable(name="policy_agent")
def policy_agent(state):
    print(">>>>>>>> NEW POLICY AGENT EXECUTED <<<<<<<<")

    question = state["question"]

    try:

        policy_type = classify_policy(question)
        print(f"0000000 [POLICY CLASSIFIER] Category = {policy_type}")

        rag_response = ask_rag(
            question,policy_type
        )

        return {

            "response":
            rag_response.get(
                "answer",
                "No answer found."
            )
        }

    except Exception as e:

        return {

            "response":
            f"RAG Error: {str(e)}"
        }