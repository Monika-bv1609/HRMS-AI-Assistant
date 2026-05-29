from fastapi import APIRouter
import xmlrpc.client

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