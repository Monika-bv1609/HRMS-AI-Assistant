import xmlrpc.client

ODOO_URL = "http://localhost:8069"

DB = "fastapi_odoo_new"

USERNAME = "admin"

PASSWORD = "admin"


def get_odoo_connection():

    common = xmlrpc.client.ServerProxy(
        f"{ODOO_URL}/xmlrpc/2/common"
    )

    uid = common.authenticate(
        DB,
        USERNAME,
        PASSWORD,
        {}
    )

    print("UID =", uid)

    return uid