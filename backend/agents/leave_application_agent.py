from memory.conversation_memory import memory_store

from services.odoo_service import (
    search_employee,
    search_leave_type,
    can_apply_leave_for_others
)


def leave_application_agent(state):

    tool_data = state["tool_data"]

    current_employee = state.get(
        "current_employee"
    )

    user_id = state.get(
        "user_id"
    )

    leave_request = tool_data.copy()

    leave_request.pop(
        "tool",
        None
    )

    if not leave_request.get(
        "employee_name"
    ):

        leave_request["employee_name"] = (
            current_employee["name"]
        )

        leave_request["employee_id"] = (
            current_employee["id"]
        )

    employee_name = leave_request.get(
        "employee_name"
    )

    leave_type_name = leave_request.get(
        "leave_type"
    )

    if leave_type_name:

        leave_types = search_leave_type(
            leave_type_name
        )

        if not leave_types:

            return {
                "response":
                f"Leave type '{leave_type_name}' not found."
            }

        leave_request["leave_type_id"] = (
            leave_types[0]["id"]
        )

    if employee_name:

        employees = search_employee(
            employee_name
        )

        if not employees:

            return {
                "response":
                f"Employee '{employee_name}' not found."
            }

        leave_request["employee_id"] = (
            employees[0]["id"]
        )

        requested_employee_id = (
            leave_request.get(
                "employee_id"
            )
        )

        current_employee_id = (
            current_employee["id"]
            if current_employee
            else None
        )

        if (
            requested_employee_id
            and current_employee_id
            and requested_employee_id != current_employee_id
        ):

            allowed = (
                can_apply_leave_for_others(
                    user_id
                )
            )

            if not allowed:

                return {
                    "response":
                    "You do not have permission to create leave for other employees."
                }

    memory_store[
        "pending_leave_request"
    ] = leave_request

    return {
        "response":
        f"""
Leave Request Summary

Employee: {leave_request.get('employee_name')}
Employee ID: {leave_request.get('employee_id')}
Leave Type: {leave_request.get('leave_type')}
Leave Type ID: {leave_request.get('leave_type_id')}
Start Date: {leave_request.get('start_date')}
End Date: {leave_request.get('end_date')}
Reason: {leave_request.get('reason')}

Please confirm.
"""
    }