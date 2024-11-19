from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from my_agent.utils.classes import routeResponse
from my_agent.utils.llms import llm
from my_agent.utils.prompts import prompt, agent_promt_template, formatted_date
from my_agent.utils.tools import tavily_tool, fake_dummy_tool

import functools

def agent_node(state, agent, name):

    if state['next'] != 'ResponderAgent':
        state['messages'] = [HumanMessage(content=state['query'])]

    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }

def supervisor_agent(state):
    supervisor_chain = prompt | llm.with_structured_output(routeResponse)
    return supervisor_chain.invoke(state)


# WeatherAgent
weather_prompt = agent_promt_template.format(agent_type = 'Weather AI Agent', formatted_date = formatted_date)
weather_agent = create_react_agent(llm, tools=[tavily_tool], state_modifier= weather_prompt)
weather_node = functools.partial(agent_node, agent=weather_agent, name="WeatherAI")

# SportsAgent
sports_prompt = agent_promt_template.format(agent_type = 'Sports AI Agent', formatted_date = formatted_date)
sports_agent = create_react_agent(llm, tools=[tavily_tool], state_modifier= sports_prompt)
sports_node = functools.partial(agent_node, agent=sports_agent, name="SportsAI")

# MarketNewsAgent
marketnews_prompt = agent_promt_template.format(agent_type = 'Market & Financial News Agent', formatted_date = formatted_date)
marketnews_agent = create_react_agent(llm, tools=[tavily_tool], state_modifier= marketnews_prompt)
marketnews_node = functools.partial(agent_node, agent=marketnews_agent, name="MarketNewsAI")

# LocalStateNews
localstatenews_prompt = agent_promt_template.format(agent_type = 'Local State News Agent', formatted_date = formatted_date)
localstatenews_agent = create_react_agent(llm, tools=[tavily_tool], state_modifier= localstatenews_prompt)
localstatenews_node = functools.partial(agent_node, agent=localstatenews_agent, name="LocalStateNewsAI")

# Responder
responder_prompt = agent_promt_template.format(agent_type = 'comprehensive response or report generator Agent', formatted_date = formatted_date)
responder_agent = create_react_agent(llm, tools = [fake_dummy_tool], state_modifier= responder_prompt)
responder_node = functools.partial(agent_node, agent=responder_agent, name="ResponderAI")