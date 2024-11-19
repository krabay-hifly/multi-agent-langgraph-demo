from pydantic import BaseModel, Field
from typing import Literal, List
from my_agent.utils.members import options

class routeResponse(BaseModel):
    next: Literal[*options]
    query: str = Field(description='Query to send to the next agent. Empty string when FINISH or ResponderAgent')
    reason: str = Field(description='The reason to why you selected the next agent')