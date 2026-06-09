from typing import TypedDict


class HRState(TypedDict):
    question: str
    tool_data: dict
    response: str
    next_agent: str
    user_id: int