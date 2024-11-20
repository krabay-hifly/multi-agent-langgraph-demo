from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from datetime import date
today = date.today()
formatted_date = today.strftime("%Y-%m-%d")

from my_agent.utils.members import members, options

# for supervisor
system_prompt = (
    "You orchestrate a team of AI agents producing a personalized daily brief for humans. "
    f"Today's date is {formatted_date}. "
    "Your AI team consists of the following AI workers: {members}. "
    "Given the following user request, you decide on the next action to take. "
    "Respond with the worker to act next, the query you're sending it and the reason behind your selection. " 
    "Each worker will perform the task (run the query you send) and respond with their results and status. " 
    "Once you collected all input to be able to answer the user's inquiry, call the FinalResponderAgent. "
    "After calling the FinalResponderAgent you MUST respond with FINISH."  
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next? "
            "Or should we FINISH? Select one of: {options}. "
            "Remember, always FINISH after FinalResponderAgent.",
        ),
    ]
).partial(
    options=str(options), 
    members=", ".join(members)
    )

# for agents
agent_promt_template = """
You are the {agent_type} in a multi-agent team producing a personal daily brief. 
Today's date is {formatted_date}. 
You're not a conversing agent, you simply complete your given assignment. 
When receiving sources from the web, remember to cite them with their URLs as hyperlinks."""