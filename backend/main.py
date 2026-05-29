from fastapi import FastAPI

from api.chat import router as chat_router
from api.upload import router as upload_router
from api.odoo import router as odoo_router

app = FastAPI()


@app.get("/")
def home():
    return {"message": "OdooHR AI Running"}


app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(odoo_router)