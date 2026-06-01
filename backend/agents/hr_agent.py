from services.llm_service import (
    classify_intent
)

from services.odoo_service import (

    get_employee_count,

    get_leaves_today,

    search_employee
)


def process_question(question: str):

    intent = classify_intent(
        question
    )

    print(f"Detected Intent: [intent]")

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

        question_lower = question.lower()

        employee_name = (

            question_lower

            .replace("find employee", "")

            .replace("search employee", "")

            .replace("employee details", "")

            .strip()
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

        return {

            "answer":
            f"{employee['name']} | {employee.get('job_title')} | {employee.get('work_email')}"
        }

    return {

        "answer":
        "I don't understand the question."
    }