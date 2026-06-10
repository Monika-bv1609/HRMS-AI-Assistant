from graph.graph_builder import graph


def ask_graph(question, user_id):

    result = graph.invoke(
        {
            "question": question,
            "user_id": user_id
        }
    )

    return result