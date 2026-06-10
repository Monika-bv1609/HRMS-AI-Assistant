from services.rag_service import (
    ask_rag
)


def policy_agent(state):
    print(">>>>>>>> NEW POLICY AGENT EXECUTED <<<<<<<<")

    question = state["question"]

    try:

        rag_response = ask_rag(
            question
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