from fastapi import FastAPI

from api.chat import router as chat_router
from api.upload import router as upload_router
from api.odoo import router as odoo_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8069",
        "http://127.0.0.1:8069",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "OdooHR AI Running"}


app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(odoo_router)