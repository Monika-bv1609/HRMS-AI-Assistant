INTENTS = {

    "employee_count": [

        "how many employees",

        "employee count",

        "total employees",

        "number of employees"
    ],

    "leave_today": [

        "who is on leave today",

        "leave today",

        "employees on leave"
    ],

    "employee_search": [

        "find employee",

        "search employee",

        "employee details"
    ]
}


def detect_intent(question: str):

    question = question.lower()

    for intent, patterns in INTENTS.items():

        for pattern in patterns:

            if pattern in question:

                return intent

    return "unknown"