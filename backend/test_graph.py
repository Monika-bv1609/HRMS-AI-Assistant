from graph.graph_builder import graph

result = graph.invoke(
    {
        "question":
        "What leave types are available?"
    }
)

print(result)