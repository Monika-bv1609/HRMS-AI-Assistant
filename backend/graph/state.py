from typing import TypedDict


class HRState(TypedDict):

    question: str

    user_id: int

    current_employee: dict

    tool_data: dict

    response: str

    next_agent: str