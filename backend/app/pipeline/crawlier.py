"""
Official surce crawler

Fetches a governement page, exrtacts, extracts its text, chunks it, embeds the chunks,
and stores them in the knowledge table.  Two safety properties:

1. DOMAIN ALLOW LIST (lega guardrail): any URL whose domain is not in
    ALLOWED_SOURCE_DOMAINS is rejected BEFORE feetching. The knowldfge base 
    canntherefore only ever contain official content.
2. CHANGE DETECTION: we hash each page; if the hash matches what's stored,
we skip re-embedding (saves time)
"""


import hashlib
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from app.core.config import ALLOWED_SOURCE_DOMAINS
from app.core.llm import embed
from app.db.database import get_connection

def is_allowed_domain(url: str) -> bool: 
    """True if the URL's domains is on the official allow list
        Accepts exact matches and subdomains (www.fns.usda.gov matches fns.usdsa.gov)
    """
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in ALLOWED_SOURCE_DOMAINS)

def extract_text(html: str) -> str:
    """Pull readable text out of an HTML page, dropping scripts/style//nav."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    return " ".join(soup.get_text(separator=" ").split())

def chunk_text(text: str, size: int = 800, overlap: int = 120) -> list[str]:
    """
    Split text into overlapping word-chunks.

    Overlap matters: if an eligibility rule straddles a chunk boundary,
    the overlap ensures at least one chunk contains the whole rule.
    """
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i : i + size]))
        i += size - overlap
    return chunks
    
    