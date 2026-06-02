from memory.conversation_memory import memory_store
from services.llm_service import client


def resolve_question(question):

    employee_name = memory_store.get(
        "employee_name"
    )

    print("=" * 50)
    print(f"MEMORY STORE: {memory_store}")
    print(f"EMPLOYEE NAME: {employee_name}")
    
    if not employee_name:
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

If the question contains references like:
- he
- him
- his
- that employee

rewrite the question using the employee name.

Return ONLY the rewritten question.

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