from dotenv import load_dotenv

load_dotenv()

from langsmith import traceable

@traceable
def test_trace():
    return "LangSmith connected"

print(test_trace())