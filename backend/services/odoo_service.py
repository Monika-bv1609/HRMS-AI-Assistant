import re

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

import dateparser

from odoo.client import get_models, DB, PASSWORD 

def resolve_date(date_value):

    if not date_value:
        return None

    if isinstance(date_value, date):
        return date_value.isoformat()

    original_value = str(date_value).strip()

    if not original_value:
        return None

    # Remove ordinal suffixes:
    # 1st -> 1, 2nd -> 2, 3rd -> 3, 17th -> 17
    cleaned_value = re.sub(
        r"(\d+)(st|nd|rd|th)\b",
        r"\1",
        original_value,
        flags=re.IGNORECASE
    )

    parsed = dateparser.parse(
        cleaned_value,
        settings={
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": datetime.now(),
            "RETURN_AS_TIMEZONE_AWARE": False,
        }
    )

    if parsed:
        return parsed.date().isoformat()

    return None

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

def get_leave_count():

    uid, models = get_models()

    return models.execute_kw(

        DB,
        uid,
        PASSWORD,

        "hr.leave",

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

    try:

        start_date = resolve_date(
            leave_request.get("start_date")
        )

        end_date = resolve_date(
            leave_request.get("end_date")
        )

        if not start_date:

            return {
                "success": False,
                "error": (
                    f"Unable to understand start date: "
                    f"{leave_request.get('start_date')}"
                )
            }

        if not end_date:

            return {
                "success": False,
                "error": (
                    f"Unable to understand end date: "
                    f"{leave_request.get('end_date')}"
                )
            }

        if end_date < start_date:

            return {
                "success": False,
                "error": "End date cannot be earlier than start date."
            }

        print(f"RESOLVED START DATE: {start_date}")
        print(f"RESOLVED END DATE: {end_date}")

        leave_vals = {

            "employee_id":
                leave_request["employee_id"],

            "holiday_status_id":
                leave_request["leave_type_id"],

            "request_date_from":
                start_date,

            "request_date_to":
                end_date,

            "name":
                leave_request.get("reason")
                or "AI Leave Request"
        }

        print(f"LEAVE PAYLOAD: {leave_vals}")

        leave_id = models.execute_kw(

            DB,

            uid,

            PASSWORD,

            "hr.leave",

            "create",

            [leave_vals]
        )

        return {

            "success": True,

            "leave_id": leave_id
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }


def get_user(user_id):

    uid, models = get_models()

    users = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "res.users",

        "read",

        [[user_id]],

        {
            "fields": [
                "name",
                "groups_id"
            ]
        }
    )

    return users[0] if users else None


def get_employee_from_user(
    user_id
):

    uid, models = get_models()

    employee = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.employee",

        "search_read",

        [[
            (
                "user_id",
                "=",
                user_id
            )
        ]],

        {
            "fields": [
                "id",
                "name"
            ],
            "limit": 1
        }
    )

    return (
        employee[0]
        if employee
        else None
    )


def get_user_group_xmlids(user_id):

    uid, models = get_models()

    user = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "res.users",

        "read",

        [[user_id]],

        {
            "fields": [
                "groups_id"
            ]
        }
    )[0]

    result = []

    for group_id in user["groups_id"]:

        xml_data = models.execute_kw(

            DB,

            uid,

            PASSWORD,

            "ir.model.data",

            "search_read",

            [[

                ("model", "=", "res.groups"),

                ("res_id", "=", group_id)

            ]],

            {

                "fields": [

                    "module",

                    "name"
                ]
            }
        )

        if xml_data:

            result.append(

                f"{xml_data[0]['module']}."
                f"{xml_data[0]['name']}"
            )

    return result


def can_apply_leave_for_others(user_id):

    xml_ids = get_user_group_xmlids(
        user_id
    )

    allowed_groups = [

        "base.group_system",

        "hr.group_hr_manager",

        "hr_holidays.group_hr_holidays_manager",

        "hr_holidays.group_hr_holidays_responsible"
    ]

    return any(
        group in xml_ids
        for group in allowed_groups
    )