from dotenv import load_dotenv

load_dotenv()
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


import os

print("LANGCHAIN_TRACING_V2 =", os.getenv("LANGCHAIN_TRACING_V2"))
print("LANGCHAIN_PROJECT =", os.getenv("LANGCHAIN_PROJECT"))
print("LANGCHAIN_API_KEY exists =", bool(os.getenv("LANGCHAIN_API_KEY")))