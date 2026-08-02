from fastapi import APIRouter

from app.agents.graph import run
from app.core.guardrails import enforce
from app.api.schemas import ChatRequest, ChatResponse, Citation


router = APIRouter()

@router.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:

    result = run(request.question)

    citations = [
        Citation(
            title=chunk.get("source_title"),
            url=chunk["source_url"],
            score=chunk["similarity"],
        )
        for chunk in result["chunks"]
    ]

    gated = enforce(result["draft"], result["chunks"])

    return ChatResponse(
        answer=gated.text,
        citations=citations,
        blocked=gated.blocked
    )