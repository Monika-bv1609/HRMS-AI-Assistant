from memory.conversation_memory import memory_store

from services.odoo_service import (
    search_employee
)


def employee_agent(state):

    tool_data = state["tool_data"]

    employee_name = tool_data.get(
        "employee_name"
    )

    request_type = tool_data.get(
        "request_type",
        "details"
    )

    if not employee_name:

        return {
            "response":
            "Unable to identify employee."
        }

    employees = search_employee(
        employee_name
    )

    if not employees:

        return {
            "response":
            "Employee not found."
        }

    employee = employees[0]

    memory_store[
        "employee_name"
    ] = employee["name"]

    if request_type == "email":

        return {

            "response":
            employee.get(
                "work_email"
            ) or "Email not available."
        }

    if request_type == "designation":

        return {

            "response":
            employee.get(
                "job_title"
            ) or "Designation not available."
        }

    return {

        "response":
        f"{employee['name']} | "
        f"{employee.get('job_title')} | "
        f"{employee.get('work_email')}"
    }