from services.odoo_service import (
    get_employee_count,
    get_leaves_today,
    search_employee
)


def process_question(question: str):

    question_lower = question.lower()

    if "how many employees" in question_lower:

        total = get_employee_count()

        return {
            "answer":
            f"There are {total} employees in the organization."
        }

    if "who is on leave today" in question_lower:

        leaves = get_leaves_today()

        if not leaves:
            return {
                "answer":
                "No employees are on leave today."
            }

        employee_names = []

        for leave in leaves:
            employee_names.append(
                leave["employee_id"][1]
            )

        return {
            "answer":
            f"Employees on leave today: {', '.join(employee_names)}"
        }

    if question_lower.startswith("find employee"):

        employee_name = question[
            len("find employee"):
        ].strip()

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