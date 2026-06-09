from services.tool_router import select_tool


def supervisor(state):

    question = state["question"]

    tool_data = select_tool(
        question
    )

    tool = tool_data.get(
        "tool"
    )

    if tool == "employee_search":

        return {

            "tool_data": tool_data,
            "next_agent": "employee"
        }
    if tool == "leave_status":

        return {
            "tool_data": tool_data,
            "next_agent": "leave"
        }

    if tool in [

        "leave_status",

        "leave_application"

    ]:

        return {

            "tool_data": tool_data,
            "next_agent": "leave"
        }

    if tool == "leave_policy":

        return {

            "tool_data": tool_data,
            "next_agent": "policy"
        }

    return {

        "response":
        "Unable to route request."
    }