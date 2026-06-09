from services.odoo_service import (
    get_leave_types,
    get_leave_type_details
)


def policy_agent(state):

    question = state["question"]

    tool_data = state["tool_data"]

    if "available" in question.lower():

        leave_types = get_leave_types()

        names = [

            leave_type["name"]

            for leave_type in leave_types
        ]

        return {

            "response":
            "Available leave types:\n\n"
            + "\n".join(
                f"• {name}"
                for name in names
            )
        }

    leave_type_name = (
        tool_data.get(
            "leave_type"
        )
    )

    if not leave_type_name:

        return {

            "response":
            "Unable to identify leave type."
        }

    leave_type = (
        get_leave_type_details(
            leave_type_name
        )
    )

    if not leave_type:

        return {

            "response":
            "Leave type not found."
        }

    return {

        "response":
        f"""
Leave Type: {leave_type['name']}

Approval: {leave_type['leave_validation_type']}
Allocation Required: {leave_type['requires_allocation']}
Request Unit: {leave_type['request_unit']}
Supporting Documents: {leave_type['support_document']}
Negative Balance Allowed: {leave_type['allows_negative']}
"""
    }