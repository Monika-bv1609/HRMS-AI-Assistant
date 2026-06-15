from services.odoo_service import (
    search_employee,
    get_employee_count
)

from memory.conversation_memory import memory_store


def employee_agent(state):

    tool_data = state["tool_data"]

    request_type = tool_data.get(
        "request_type"
    )

    if request_type == "count":

        total = get_employee_count()

        return {
            "response":
            f"Total employees: {total}"
        }

    employee_name = tool_data.get(
        "employee_name"
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
            f"Employee '{employee_name}' not found."
        }

    employee = employees[0]

    memory_store["employee_name"] = employee["name"]

    if request_type == "email":

        return {
            "response":
            employee.get("work_email")
            or "Email not available."
        }

    if request_type in [
        "designation",
        "job_title",
        "role"
    ]:

        return {
            "response":
            employee.get("job_title")
            or "Designation not available."
        }

    return {
        "response":
        f"{employee['name']} | "
        f"{employee.get('job_title')} | "
        f"{employee.get('work_email')}"
    }