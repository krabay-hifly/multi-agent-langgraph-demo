from pydantic import BaseModel, Field
from typing import Literal, List
from my_agent.utils.members import options

class routeResponse(BaseModel):
    next: Literal[*options]
    query: str = Field(description="Query to send to the next agent. Including today's date can be helpful. Empty string when FINISH or FinalResponderAgent. Always FINISH after FinalResponderAgent.")
    reason: str = Field(description='The reason to why you selected the next agent')