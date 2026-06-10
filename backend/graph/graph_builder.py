from langgraph.graph import (
    StateGraph,
    START,
    END
)
from agents.leave_application_agent import (
    leave_application_agent
)

from graph.state import HRState

from graph.supervisor import (
    supervisor
)

from agents.employee_agent import (
    employee_agent
)
from agents.leave_agent import (
    leave_agent
)
from agents.policy_agent import policy_agent

graph_builder = StateGraph(
    HRState
)

graph_builder.add_node(
    "supervisor",
    supervisor
)

graph_builder.add_node(
    "employee",
    employee_agent
)

graph_builder.add_node(
    "leave",
    leave_agent
)

graph_builder.add_node(
    "policy",
    policy_agent
)
graph_builder.add_node(
    "leave_application",
    leave_application_agent
)

graph_builder.add_edge(
    START,
    "supervisor"
)



graph_builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next_agent"],
    {
        "employee": "employee",
        "leave": "leave",
        "policy": "policy",
        "leave_application": "leave_application"
    }
)

graph_builder.add_edge(
    "leave_application",
    END
)

graph = graph_builder.compile()