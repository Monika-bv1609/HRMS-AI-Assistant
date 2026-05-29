import xmlrpc.client

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