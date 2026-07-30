from app.pipeline.crawler import search_knowledge

def retrieve(question: str, min_score: float = 0.3) -> list[dict]:
    """
    Return knwoledge base chunks relevant to the question, filtering out
    weak matches so the Eligibility Agent never reasons form irrelevant
    or barely-related context.
    """
    results = search_knowledge(question)

    filtered = [
        result
        for result in results
        if result["similarity"] >= min_score
    ]

    return filtered