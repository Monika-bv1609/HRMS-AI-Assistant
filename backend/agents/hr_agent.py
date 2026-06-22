

from memory.context_resolver import (
    resolve_question
)

from memory.conversation_memory import (
    memory_store
)



from services.odoo_service import (
    create_leave_request,
    get_user,
    get_employee_from_user,
)


from graph.graph_builder import graph



from services.confirmation_classifier import (
    classify_confirmation
)

from langsmith import traceable

@traceable(name="process_hr_question")
def process_question(question: str, user_id: int = None):

    print("=" * 50)
    print(f"ORIGINAL QUESTION: [{question}]")
    print(f"CURRENT USER ID: {user_id}")

    current_user = get_user(
        user_id
    )

    print(
        f"//////// CURRENT USER: {current_user}"
    )

    current_employee = (
        get_employee_from_user(
            user_id
        )
    )

    pending_leave = memory_store.get(
        "pending_leave_request"
    )

    if pending_leave:

        confirmation = classify_confirmation(
            question
        )

        if confirmation == "YES":

            result = create_leave_request(
                pending_leave
            )

            memory_store[
                "pending_leave_request"
            ] = None

            if not result["success"]:

                return {
                    "answer":
                    f"Unable to create leave.\n\n{result['error']}"
                }

            return {
                "answer":
                f"Leave request created successfully. Leave ID: {result['leave_id']}"
            }

        elif confirmation == "NO":

            memory_store[
                "pending_leave_request"
            ] = None

            return {
                "answer":
                "Leave request cancelled."
            }

    question = resolve_question(
        question
    )

    print(
        f"QUESTION AFTER RESOLUTION: [{question}]"
    )

    graph_result = graph.invoke(
        {
            "question": question,
            "user_id": user_id,
            "current_employee": current_employee
        },
        config={
            "run_name": "hr_chat_request",
            "metadata": {
                "user_id": user_id,
                "employee_id": current_employee.get("id") if current_employee else None
            },
            "configurable": {
                "thread_id": str(user_id)
            }
        }
    )

    return {
        "answer": graph_result.get(
            "response",
            "Unable to process request."
        ),
        "agent": graph_result.get(
            "next_agent"
        )
    }