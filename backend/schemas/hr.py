from pydantic import BaseModel

class HRQuestion(BaseModel):

    question: str

    user_id: int | None = None