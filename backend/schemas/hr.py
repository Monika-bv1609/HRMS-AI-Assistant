from pydantic import BaseModel

class HRQuestion(BaseModel):
    question: str