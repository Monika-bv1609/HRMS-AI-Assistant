from services.odoo_service import (
    is_employee_on_leave_today,
    get_leave_count,
    get_leaves_today
)

from langsmith import traceable

@traceable(name="leave_agent")
def leave_agent(state):

    tool_data = state["tool_data"]

    request_type = tool_data.get(
        "request_type"
    )

    if request_type == "count":

        total = get_leave_count()

        return {

            "response":
            f"Total leave requests: {total}"
        }

    if request_type == "today_list":

        leaves = get_leaves_today()

        if not leaves:

            return {

                "response":
                "No employees are on leave today."
            }

        employee_names = []

        for leave in leaves:

            employee_names.append(
                leave["employee_id"][1]
            )

        return {

            "response":
            "Employees on leave today:\n\n"
            + "\n".join(
                f"• {name}"
                for name in employee_names
            )
        }

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