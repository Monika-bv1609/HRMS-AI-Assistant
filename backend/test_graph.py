from graph.graph_builder import graph

result = graph.invoke({

    "question":
    "Apply leave for me tomorrow",

    "user_id":
    2,

    "current_employee":
    {
        "id": 1,
        "name": "Mitchell Admin"
    }
})

print(result)