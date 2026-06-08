from memory.conversation_memory import memory_store
from services.llm_service import client


def resolve_question(question):

    employee_name = memory_store.get(
        "employee_name"
    )

    print("=" * 50)
    print(f"MEMORY STORE: {memory_store}")
    print(f"EMPLOYEE NAME: {employee_name}")

    question_lower = f" {question.lower()} "

    # Self references should never be rewritten
    if (
        " me " in question_lower
        or " my " in question_lower
        or " myself " in question_lower
        or " i " in question_lower
    ):
        return question

    # No employee in memory
    if not employee_name:
        return question

    # Employee lookup questions should not be rewritten
    if (
        question_lower.strip().startswith("who is")
        or " email" in question_lower
        or " designation" in question_lower
    ):
        return question

    # Only invoke resolver if pronouns exist
    pronouns = [
        " he ",
        " him ",
        " his ",
        " she ",
        " her ",
        " that employee "
    ]

    if not any(
        pronoun in question_lower
        for pronoun in pronouns
    ):
        return question

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content": f"""
You are a context resolver.

Last employee discussed:
{employee_name}

Only rewrite the question when it contains:
- he
- him
- his
- she
- her
- that employee

Replace those references with the employee name.

Never rewrite:
- me
- my
- myself
- I

Those always refer to the logged-in user.

Return only the rewritten question.

If no rewrite is needed,
return the original question.
"""
            },

            {
                "role": "user",
                "content": question
            }

        ],

        temperature=0
    )

    resolved_question = (

        response
        .choices[0]
        .message
        .content
        .strip()
    )

    print(
        f"Resolved Question: {resolved_question}"
    )

    return resolved_question