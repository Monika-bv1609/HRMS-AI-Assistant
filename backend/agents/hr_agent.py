from services.llm_service import (
    classify_intent
)

from memory.context_resolver import (
    resolve_question
)

from memory.conversation_memory import (
    memory_store
)

from services.odoo_service import (

    get_employee_count,

    get_leaves_today,

    search_employee
)


def process_question(question: str):

    print("=" * 50)
    print(f"ORIGINAL QUESTION: [{question}]")

    question = resolve_question(
        question
    )

    print(
        f"QUESTION AFTER RESOLUTION: [{question}]"
    )

    intent = classify_intent(
        question
    )

    print(f"INTENT: [{intent}]")

    if intent == "employee_count":

        total = get_employee_count()

        return {

            "answer":
            f"There are {total} employees in the organization."
        }

    if intent == "leave_today":

        leaves = get_leaves_today()

        if not leaves:

            return {

                "answer":
                "No employees are on leave today."
            }

        employee_names = [

            leave["employee_id"][1]

            for leave in leaves
        ]

        return {

            "answer":
            f"Employees on leave today: {', '.join(employee_names)}"
        }

    if intent == "employee_search":

        question_lower = (
            question.lower()
        )

        if "find employee" in question_lower:

            employee_name = (
                question_lower
                .replace(
                    "find employee",
                    ""
                )
                .strip()
                .rstrip(".!?")
            )

        elif "search employee" in question_lower:

            employee_name = (
                question_lower
                .replace(
                    "search employee",
                    ""
                )
                .strip()
                .rstrip(".!?")
            )

        elif "employee details" in question_lower:

            employee_name = (
                question_lower
                .replace(
                    "employee details",
                    ""
                )
                .strip()
                .rstrip(".!?")
            )

        else:

            employee_name = (
                memory_store.get(
                    "employee_name"
                )
            )

        print(
            f"EXTRACTED EMPLOYEE: [{employee_name}]"
        )

        employees = search_employee(
            employee_name
        )

        if not employees:

            return {

                "answer":
                "Employee not found."
            }

        employee = employees[0]

        memory_store[
            "employee_name"
        ] = employee["name"]

        print(
            f"MEMORY UPDATED: {memory_store}"
        )

        return {

            "answer":
            f"{employee['name']} | {employee.get('job_title')} | {employee.get('work_email')}"
        }

    return {

        "answer":
        "I don't understand the question."
    }