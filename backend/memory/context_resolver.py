from memory.conversation_memory import memory_store
from services.llm_service import client


import re


def resolve_question(question):

    employee_name = memory_store.get(
        "employee_name"
    )

    print("=" * 50)
    print(f"MEMORY STORE: {memory_store}")
    print(f"EMPLOYEE NAME: {employee_name}")

    question_lower = f" {question.lower()} "

    if (
        " me " in question_lower
        or " my " in question_lower
        or " myself " in question_lower
        or " i " in question_lower
    ):
        return question

    if not employee_name:
        return question

    pronoun_pattern = (
        r"\b(he|him|his|she|her|that employee)\b"
    )

    if not re.search(
        pronoun_pattern,
        question,
        flags=re.IGNORECASE
    ):
        return question

    resolved_question = re.sub(
        pronoun_pattern,
        employee_name,
        question,
        flags=re.IGNORECASE
    )

    print(
        f"Resolved Question: {resolved_question}"
    )

    return resolved_question