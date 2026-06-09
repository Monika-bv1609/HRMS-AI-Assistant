from graph.graph_builder import graph

questions = [
    "Who is Rachel Perry?",
    "Rachel Perry email",
    "Is Rachel Perry on leave today?",
    "What leave types are available?",
    "Tell me about Sick Time Off"
]

for question in questions:

    print("\n" + "=" * 60)
    print(f"QUESTION: {question}")

    result = graph.invoke(
        {
            "question": question
        }
    )

    print(f"Agent: {result['next_agent']}")
    print(f"Response: {result['response']}")