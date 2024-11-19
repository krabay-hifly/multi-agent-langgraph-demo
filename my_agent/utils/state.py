import operator
from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated, Sequence


class AgentState(TypedDict):

    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    query: str
    reason: str