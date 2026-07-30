from groq import Groq

from app.agents.prompts import ELIGIBILITY_SYSTEM_PROMPT
from app.core.config import get_groq_api_key


def eligibility(question: str, chunks: list[dict]) -> str:
    """Answer a user question using only the retrieved official source passages."""

    context = "\n\n".join(
        f"""
        Source {i + 1}
        Title: {chunk['source_title']}
        URL: {chunk['source_url']}
        Content: {chunk['chunk_text']}
        """
        for i, chunk in enumerate(chunks)
    )

    if not context:
        context = "No official sources were retrieved."

    system_prompt = ELIGIBILITY_SYSTEM_PROMPT.format(context=context)

    client = Groq(api_key=get_groq_api_key())

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )

    return response.choices[0].message.content