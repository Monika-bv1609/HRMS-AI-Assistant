from fastapi import APIRouter
import xmlrpc.client
from datetime import date
from schemas.hr import HRQuestion
from agents.hr_agent import process_question

router = APIRouter()

ODOO_URL = "http://localhost:8069"
DB = "fastapi_odoo_new"
USERNAME = "admin"
PASSWORD = "admin"


def get_models():

    common = xmlrpc.client.ServerProxy(
        f"{ODOO_URL}/xmlrpc/2/common"
    )

    uid = common.authenticate(
        DB,
        USERNAME,
        PASSWORD,
        {}
    )

    models = xmlrpc.client.ServerProxy(
        f"{ODOO_URL}/xmlrpc/2/object"
    )

    return uid, models


@router.get("/employees")
def get_employees():

    uid, models = get_models()

    employees = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        'hr.employee',

        'search_read',

        [[]],

        {
            'fields': [
                'name'
            ]
        }
    )

    return employees


@router.get("/employees/count")
def get_employee_count():

    uid, models = get_models()

    total = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.employee",

        "search_count",

        [[]]
    )

    return {

        "total_employees": total
    }



@router.get("/employee/{employee_id}")
def get_employee(employee_id: int):

    uid, models = get_models()

    employee = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.employee",

        "read",

        [[employee_id]],

        {
            "fields": [
                "name",
                "work_email",
                "job_title"
            ]
        }
    )

    if not employee:

        return {
            "message": "Employee not found"
        }

    return employee[0]


@router.get("/employees/search")
def search_employees(name: str):

    uid, models = get_models()

    employees = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.employee",

        "search_read",

        [
            [
                ("name", "ilike", name)
            ]
        ],

        {
            "fields": [
                "name",
                "work_email",
                "job_title"
            ]
        }
    )

    return employees


@router.get("/leaves")
def get_leaves():

    uid, models = get_models()

    leaves = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.leave",

        "search_read",

        [[]],

        {
            "fields": [
                "employee_id",
                "holiday_status_id",
                "request_date_from",
                "request_date_to",
                "state"
            ]
        }
    )

    return leaves


@router.get("/leaves/count")
def get_leave_count():

    uid, models = get_models()

    total = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "hr.leave",

        "search_count",

        [[]]
    )

    return {

        "total_leaves": total
    }



@router.get("/leaves/today")
def get_leaves_today():

    uid, models = get_models()

    today = str(date.today())

    leaves = models.execute_kw(

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

                "holiday_status_id",

                "request_date_from",

                "request_date_to"

            ]
        }
    )

    return leaves


@router.post("/ask-hr")
def ask_hr(data: HRQuestion):

    result = process_question(
        data.question
    )

    return result



@router.get("/leave-types")
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

@router.get("/test-create-leave")
def test_create_leave():

    from services.odoo_service import (
        create_test_leave
    )

    leave_id = create_test_leave()

    return {
        "leave_id": leave_id
    }

    return leave_types


@router.get("/users")
def get_users():

    uid, models = get_models()

    users = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "res.users",

        "search_read",

        [[]],

        {
            "fields": [
                "name",
                "groups_id"
            ]
        }
    )

    return users


@router.get("/groups")
def get_groups():

    uid, models = get_models()

    groups = models.execute_kw(

        DB,

        uid,

        PASSWORD,

        "res.groups",

        "search_read",

        [[]],

        {
            "fields": [
                "name",
                "category_id"
            ]
        }
    )

    return groups



@router.get("/group-xmlids")
def get_group_xmlids():

    uid, models = get_models()

    records = models.execute_kw(

        DB,
        uid,
        PASSWORD,

        "ir.model.data",

        "search_read",

        [[
            ("model", "=", "res.groups")
        ]],

        {
            "fields": [
                "module",
                "name",
                "res_id"
            ],
            "limit": 100
        }
    )

    return records