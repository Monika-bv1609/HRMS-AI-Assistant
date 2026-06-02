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