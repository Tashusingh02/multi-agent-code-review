from pydantic import BaseModel
from typing import Optional

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    focus: Optional[str] = None

class AgentResult(BaseModel):
    agent: str
    output: str

class CodeReviewResponse(BaseModel):
    review: AgentResult
    tests: AgentResult
    improved_code: AgentResult
    summary: str