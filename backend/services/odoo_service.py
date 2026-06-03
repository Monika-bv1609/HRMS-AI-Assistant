from datetime import date

from odoo.client import (
    get_models,
    DB,
    PASSWORD
)


def get_employee_count():

    uid, models = get_models()

    return models.execute_kw(
        DB,
        uid,
        PASSWORD,
        "hr.employee",
        "search_count",
        [[]]
    )


def get_leaves_today():

    uid, models = get_models()

    today = str(date.today())

    return models.execute_kw(
        DB,
        uid,
        PASSWORD,
        "hr.leave",
        "search_read",
        [[
            ("request_date_from", "<=", today),
            ("request_date_to", ">=", today),
            ("state", "=", "validate")
        ]],
        {
            "fields": [
                "employee_id",
                "holiday_status_id"
            ]
        }
    )


def search_employee(name):

    uid, models = get_models()

    return models.execute_kw(
        DB,
        uid,
        PASSWORD,
        "hr.employee",
        "search_read",
        [[
            ("name", "ilike", name)
        ]],
        {
            "fields": [
                "name",
                "work_email",
                "job_title"
            ]
        }
    )


def get_leave_count_today():

    leaves = get_leaves_today()

    return len(leaves)



def is_employee_on_leave_today(
    employee_name
):

    leaves = get_leaves_today()

    for leave in leaves:

        employee = leave[
            "employee_id"
        ][1]

        if (
            employee.lower()
            ==
            employee_name.lower()
        ):

            return True

    return False


def get_leave_types():

    uid, models = get_models()

    leave_types = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.leave.type",

        "search_read",

        [[]],

        {
            "fields": [

                "name",

                "leave_validation_type",

                "requires_allocation",

                "allocation_validation_type",

                "request_unit",

                "employee_requests",

                "unpaid",

                "support_document",

                "allows_negative"
            ]
        }
    )

    return leave_types


def get_leave_type_details(
    leave_type_name
):

    leave_types = get_leave_types()

    for leave_type in leave_types:

        if (

            leave_type["name"]
            .lower()

            ==

            leave_type_name
            .lower()

        ):

            return leave_type

    return None


def create_test_leave():

    uid, models = get_models()

    leave_id = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.leave",

        "create",

        [{

            "employee_id": 1,
            "holiday_status_id": 2,
            "request_date_from": "2026-06-03",
            "request_date_to": "2026-06-03",
            "name": "AI Test Leave"
        }]
    )

    return leave_id



def search_leave_type(leave_type_name):

    uid, models = get_models()

    leave_types = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.leave.type",

        "search_read",

        [[

            ("name", "ilike", leave_type_name)

        ]],

        {

            "fields": [

                "name"
            ]
        }
    )

    return leave_types


def create_leave_request(leave_request):

    uid, models = get_models()

    leave_id = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.leave",

        "create",

        [[{

            "employee_id":
            leave_request["employee_id"],

            "holiday_status_id":
            leave_request["leave_type_id"],

            "request_date_from":
            leave_request["start_date"],

            "request_date_to":
            leave_request["end_date"],

            "name":
            leave_request.get("reason")
            or "AI Leave Request"
        }]]
    )

    return leave_id