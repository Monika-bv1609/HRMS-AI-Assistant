from services.llm_service import (
    classify_intent
)

from memory.context_resolver import (
    resolve_question
)

from memory.conversation_memory import (
    memory_store
)

from services.rag_service import ask_rag


from services.odoo_service import (

    get_employee_count,

    get_leaves_today,

    search_employee,
    search_leave_type,
    create_leave_request,
    get_user,
    get_employee_from_user,
    can_apply_leave_for_others

)


from services.odoo_service import (
    get_leave_count_today,
    is_employee_on_leave_today
)



from services.odoo_service import (
    get_leave_types,
    get_leave_type_details
)



from services.confirmation_classifier import (
    classify_confirmation
)

def process_question(question: str, user_id: int = None):

    print("=" * 50)
    print(f"ORIGINAL QUESTION: [{question}]")
    print(f"CURRENT USER ID: {user_id}")

    current_user = get_user(
        user_id
    )

    print(
        f"//////// CURRENT USER: {current_user}"
    )

    current_employee = (
        get_employee_from_user(
            user_id
        )
    )

    print(
        f"CURRENT EMPLOYEE: {current_employee}"
    )

    pending_leave = memory_store.get(
        "pending_leave_request"
    )

    if pending_leave:

        confirmation = classify_confirmation(
            question
        )

        if confirmation == "YES":

            result = create_leave_request(
                pending_leave
            )

            memory_store[
                "pending_leave_request"
            ] = None

            if not result["success"]:

                return {

                    "answer":
                    f"Unable to create leave.\n\n{result['error']}"
                }

            return {

                "answer":
                f"Leave request created successfully. Leave ID: {result['leave_id']}"
            }

        elif confirmation == "NO":

            memory_store[
                "pending_leave_request"
            ] = None

            return {

                "answer":
                "Leave request cancelled."
            }
            

        question = resolve_question(
            question
        )

    print(
        f"QUESTION AFTER RESOLUTION: [{question}]"
    )

    from services.tool_router import (
        select_tool
    )


    tool_data = select_tool(
        question
    )


    print(
        f"TOOL DATA: {tool_data}"
    )

    intent = tool_data.get(
        "tool"
    )

    print(f"TOOL: [{intent}]")

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

        employee_name = tool_data.get(
            "employee_name"
        )

        request_type = tool_data.get(
            "request_type",
            "details"
        )

        print(
            f"EMPLOYEE NAME: {employee_name}"
        )

        if not employee_name:

            return {

                "answer":
                "Unable to identify employee."
            }

        employees = search_employee(
            employee_name
        )

        if not employees:

            return {

                "answer":
                "Employee not found."
            }

        employee = employees[0]

        memory_store[
            "employee_name"
        ] = employee["name"]

        print(
            f"MEMORY UPDATED: {memory_store}"
        )

        if request_type == "email":

            return {

                "answer":
                employee.get(
                    "work_email"
                ) or "Email not available."
            }

        if request_type == "designation":

            return {

                "answer":
                employee.get(
                    "job_title"
                ) or "Designation not available."
            }

        return {

            "answer":
            f"{employee['name']} | {employee.get('job_title')} | {employee.get('work_email')}"
        }
    


    if intent == "leave_count":

        total = get_leave_count_today()

        return {

            "answer":
            f"{total} employees are on leave today."
        }


    if intent == "leave_status":

        employee_name = tool_data.get(
            "employee_name"
        )

        if not employee_name:

            employee_name = (
                memory_store.get(
                    "employee_name"
                )
            )

        if not employee_name:

            return {

                "answer":
                "Unable to identify employee."
            }

        on_leave = (
            is_employee_on_leave_today(
                employee_name
            )
        )

        if on_leave:

            return {

                "answer":
                f"{employee_name} is on leave today."
            }

        return {

            "answer":
            f"{employee_name} is not on leave today."
        }
    

    if intent == "leave_policy":

        print(">>>>>>>> NEW POLICY AGENT EXECUTED <<<<<<<<")

        try:

            rag_response = ask_rag(
                question
            )

            print(
                f"RAG RESPONSE: {rag_response}"
            )

            return {

                "answer":
                rag_response.get(
                    "answer",
                    "No answer found."
                )
            }

        except Exception as e:

            return {

                "answer":
                f"RAG Error: {str(e)}"
            }
    

    if intent == "leave_application":

        leave_request = tool_data.copy()

        leave_request.pop(
            "tool",
            None
        )

        print(
            f"LEAVE REQUEST FROM ROUTER: {leave_request}"
        )
    
        if not leave_request.get(
            "employee_name"
        ):

            leave_request[
                "employee_name"
            ] = current_employee["name"]

            leave_request[
                "employee_id"
            ] = current_employee["id"]

            print(
                f"SELF LEAVE DETECTED: "
                f"{current_employee['name']}"
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

                    "answer":
                    f"Leave type '{leave_type_name}' not found."
                }

            leave_request[
                "leave_type_id"
            ] = leave_types[0]["id"]

            print(
                f"LEAVE TYPE RESOLVED: {leave_types[0]['id']}"
            )

        if employee_name:

            employees = search_employee(
                employee_name
            )

            if not employees:

                return {

                    "answer":
                    f"Employee '{employee_name}' not found."
                }

            leave_request[
                "employee_id"
            ] = employees[0]["id"]

            print(
                f"EMPLOYEE RESOLVED: {employees[0]['id']}"
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

                and

                current_employee_id

                and

                requested_employee_id
                !=
                current_employee_id
            ):

                allowed = (
                    can_apply_leave_for_others(
                        user_id
                    )
                )

                if not allowed:

                    return {

                        "answer":
                        "You do not have permission to create leave for other employees."
                    }

        memory_store[
            "pending_leave_request"
        ] = leave_request

        print(
            f"PENDING LEAVE: {memory_store['pending_leave_request']}"
        )

        if not leave_request:

            return {

                "answer":
                "Unable to understand leave request."
            }

        return {

            "answer":
            f"""
        Leave Request Summary

        Employee: {leave_request.get('employee_name')}
        Employee ID: {leave_request.get('employee_id')}
        Leave Type: {leave_request.get('leave_type')}
        Leave Type ID:{leave_request.get('leave_type_id')}
        Start Date: {leave_request.get('start_date')}
        End Date: {leave_request.get('end_date')}
        Reason: {leave_request.get('reason')}

        Please confirm.
        """
        }


    return {

        "answer":
        "I don't understand the question."
    }