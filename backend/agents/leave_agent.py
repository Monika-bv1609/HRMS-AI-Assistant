from services.odoo_service import (
    is_employee_on_leave_today
)


def leave_agent(state):

    tool_data = state["tool_data"]

    employee_name = tool_data.get(
        "employee_name"
    )

    if not employee_name:

        return {
            "response":
            "Unable to identify employee."
        }

    on_leave = (
        is_employee_on_leave_today(
            employee_name
        )
    )

    if on_leave:

        return {
            "response":
            f"{employee_name} is on leave today."
        }

    return {
        "response":
        f"{employee_name} is not on leave today."
    }