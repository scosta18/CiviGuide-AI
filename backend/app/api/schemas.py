from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)

class Citation(BaseModel):
    title: str | None = None
    url: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    citaitons: list[Citation]
    blocked: bool 