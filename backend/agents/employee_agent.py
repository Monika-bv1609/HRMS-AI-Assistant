from services.odoo_service import (
    search_employee,
    get_employee_count
)


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

    return {

        "response":
        f"{employee['name']} | "
        f"{employee.get('job_title')} | "
        f"{employee.get('work_email')}"
    }