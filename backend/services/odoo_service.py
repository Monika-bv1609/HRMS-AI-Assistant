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