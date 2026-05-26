from fastapi import FastAPI

from api.chat import router as chat_router

app = FastAPI()


@app.get("/")
def home():
    return {"message": "OdooHR AI Running"}


app.include_router(chat_router)