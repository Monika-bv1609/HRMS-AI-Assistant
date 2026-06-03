from services.llm_service import (
    classify_intent
)

from memory.context_resolver import (
    resolve_question
)

from memory.conversation_memory import (
    memory_store
)

from services.employee_entity_extractor import (
    extract_employee_entity
)

from services.odoo_service import (

    get_employee_count,

    get_leaves_today,

    search_employee
)

from services.leave_entity_extractor import (
    extract_leave_entity
)

from services.odoo_service import (
    get_leave_count_today,
    is_employee_on_leave_today
)

from services.leave_policy_entity_extractor import (
    extract_leave_policy_entity
)

from services.odoo_service import (
    get_leave_types,
    get_leave_type_details
)

from services.leave_application_entity_extractor import (
    extract_leave_application
)

def process_question(question: str):

    print("=" * 50)
    print(f"ORIGINAL QUESTION: [{question}]")

    if question.lower() in [

        "yes",

        "confirm",

        "proceed",

        "submit"
    ]:

        pending_leave = (

            memory_store.get(
                "pending_leave_request"
            )
        )

        if not pending_leave:

            return {

                "answer":
                "No pending leave request found."
            }

        return {

            "answer":
            f"""
Pending Leave Found

Leave Type: {pending_leave['leave_type']}
Start Date: {pending_leave['start_date']}
End Date: {pending_leave['end_date']}
Reason: {pending_leave['reason']}
"""
        }

    question = resolve_question(
        question
    )

    print(
        f"QUESTION AFTER RESOLUTION: [{question}]"
    )

    intent = classify_intent(
        question
    )

    print(f"INTENT: [{intent}]")

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

        entity = extract_employee_entity(
            question
        )

        print(
            f"EXTRACTED ENTITY: {entity}"
        )

        employee_name = entity.get(
            "employee_name"
        )

        request_type = entity.get(
            "request_type",
            "details"
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

        entity = extract_leave_entity(
            question
        )

        employee_name = entity.get(
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

        if "available" in question.lower():

            leave_types = get_leave_types()

            names = [

                leave_type["name"]

                for leave_type in leave_types
            ]

            return {

                "answer":
                "Available leave types:\n\n"
                + "\n".join(
                    f"• {name}"
                    for name in names
                )
            }

        entity = (
            extract_leave_policy_entity(
                question
            )
        )

        leave_type_name = (
            entity.get(
                "leave_type"
            )
        )

        if not leave_type_name:

            return {

                "answer":
                "Unable to identify leave type."
            }

        leave_type = (
            get_leave_type_details(
                leave_type_name
            )
        )

        if not leave_type:

            return {

                "answer":
                "Leave type not found."
            }

        return {

            "answer":
            f"""
    Leave Type: {leave_type['name']}

    Approval: {leave_type['leave_validation_type']}
    Allocation Required: {leave_type['requires_allocation']}
    Request Unit: {leave_type['request_unit']}
    Supporting Documents: {leave_type['support_document']}
    Negative Balance Allowed: {leave_type['allows_negative']}
    """
        }
    

    if intent == "leave_application":

        leave_request = (
            extract_leave_application(
                question
            )
        )

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

    Leave Type: {leave_request['leave_type']}
    Start Date: {leave_request['start_date']}
    End Date: {leave_request['end_date']}
    Reason: {leave_request['reason']}

    Please confirm.
    """
        }

    if question.lower() in [

        "yes",

        "confirm",

        "proceed",

        "submit"
    ]:

        pending_leave = (

            memory_store.get(
                "pending_leave_request"
            )
        )

        if not pending_leave:

            return {

                "answer":
                "No pending leave request found."
            }

        return {

            "answer":
            f"""
Pending Leave Found

Leave Type: {pending_leave['leave_type']}
Start Date: {pending_leave['start_date']}
End Date: {pending_leave['end_date']}
Reason: {pending_leave['reason']}
"""
        }

    return {

        "answer":
        "I don't understand the question."
    }