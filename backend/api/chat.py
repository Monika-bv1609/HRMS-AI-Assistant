from fastapi import APIRouter

from schemas.chat_schema import QuestionRequest
from services.chat_service import process_question

router = APIRouter()


@router.post("/ask")
def ask_question(data: QuestionRequest):
    return process_question(data.question)