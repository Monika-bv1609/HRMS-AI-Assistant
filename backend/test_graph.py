from graph.graph_builder import graph

result = graph.invoke(
    {
        "question":
        "Is Rachel Perry on leave today?"
    }
)

print(result)