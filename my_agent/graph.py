from dotenv import load_dotenv
load_dotenv()

from my_agent.utils.state import AgentState
from my_agent.utils.members import members
from my_agent.utils.nodes import supervisor_agent, weather_node, sports_node, marketnews_node, localstatenews_node, responder_node

from langgraph.graph import END, StateGraph, START

# GRAPH
workflow = StateGraph(AgentState)

workflow.add_node("WeatherAgent", weather_node)
workflow.add_node("SportsAgent", sports_node)
workflow.add_node("MarketNewsAgent", marketnews_node)
workflow.add_node("LocalStateNewsAgent", localstatenews_node)
workflow.add_node("ResponderAgent", responder_node)
workflow.add_node("supervisor", supervisor_agent)

for member in members:
    # We want our workers to ALWAYS "report back" to the supervisor when done
    workflow.add_edge(member, "supervisor")

# The supervisor populates the "next" field in the graph state
# which routes to a node or finishes
conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)

# Finally, add entrypoint
workflow.add_edge(START, "supervisor")

graph = workflow.compile()