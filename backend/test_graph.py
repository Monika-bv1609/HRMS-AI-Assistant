from graph.graph_builder import graph

questions = [

    "What is the notice period?",

    "Can I work from home?",

    "What is paternity leave?"
]

for question in questions:

    print("\n" + "=" * 60)

    result = graph.invoke({

        "question": question
    })

    print(result)