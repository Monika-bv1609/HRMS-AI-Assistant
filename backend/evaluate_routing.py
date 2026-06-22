from dotenv import load_dotenv
load_dotenv()

from langsmith import evaluate
from memory.conversation_memory import memory_store
from agents.hr_agent import process_question

def predict(inputs: dict) -> dict:
    memory_store.clear()

    return process_question(
        question=inputs["question"],
        user_id=inputs["user_id"]
    )


def exact_match(outputs: dict, reference_outputs: dict) -> bool:
    return outputs.get("agent") == reference_outputs.get("agent")


results = evaluate(
    predict,
    data="hrms-test-cases",
    evaluators=[exact_match],
    experiment_prefix="routing-evaluation"
)

print(results)