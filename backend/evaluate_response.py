from langsmith import evaluate

from agents.hr_agent import process_question


def keyword_match(outputs, reference_outputs):

    answer = outputs["answer"].lower()

    expected = reference_outputs["expected_keyword"].lower()

    return expected in answer


evaluate(
    lambda inputs: process_question(
        question=inputs["input"],
        user_id=2
    ),
    data="hrms-response-evalution",
    evaluators=[keyword_match],
    experiment_prefix="response-evaluation"
)