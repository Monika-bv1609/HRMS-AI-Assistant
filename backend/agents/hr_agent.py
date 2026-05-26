def hr_policy_agent(question: str):

    question = question.lower()

    if "leave" in question:
        return "Employees get 12 annual leaves."

    elif "maternity" in question:
        return "Maternity leave policy allows 6 months leave."

    elif "work from home" in question:
        return "Employees can work from home 2 days a week."

    return "Sorry, policy not found."