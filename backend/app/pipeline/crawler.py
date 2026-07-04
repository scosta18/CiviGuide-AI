import hashlib
import os
from urllib.parse import urlparse

import httpx
import psycopg
from bs4 import BeautifulSoup
from sentence_transformers  import SentenceTransformer
from app.db.database import get_connection


ALLOWLISTED_DOMAINS = {
    "dhs.maryland.gov",
    "benefits.maryland.gov",
}

model = SentenceTransformer('all-MiniLM-L6-v2')

def is_allowed_url(url: str) -> bool:
    domain = urlparse(url).netloc.lower()
    return domain in ALLOWLISTED_DOMAINS

def fetch_official_page(url: str) -> tuple[str, str]:
    if not is_allowed_url(url):
        raise ValueError(f"Rejected non-allow-listed dmain: {url}")
    
    response = httpx.get(url, timeout=10, follow_redirects=True)
    response.raise_for_status()

    final_url = str(response.url)
    if not is_allowed_url(final_url):
        raise ValueError(f"Rejected non-allow-listed dmain: {final_url}")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else url
    text = " ".join(soup.stripped_strings)

    return title, text

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    """turning long sentances into small segments and adding them into chunk"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def already_crawled_unchanged(url: str, content_hash: str) -> bool:
    #conncet DB first
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
            "SELECT content_hash FROM crawler_logs WHERE source_url = %s",
            (url,),
)
            row = cur.fetchone()

    return row is not None and row[0] == content_hash

def store_chunks(url: str, title: str, chunks:list[str], content_hash: str):
    embedding = model.encode(chunks).tolist()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM knowledge WHERE source_url = %s", (url,))

            for index, chunk in enumerate(chunks):
                cur.execute(
                    """
                    INSERT INTO knowledge
                    (source_url, source_title, chunk_index, chunk_text, embedding, content_hash)
                    VALUES(%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        url,
                        title,
                        index,
                        chunk,
                        embedding[index],
                        content_hash
                    ),
                )

                cur.execute(
                    """
                    INSERT INTO crawler_logs
                    (source_url, content_hash, status, message)
                    VALUES(%s, %s, %s, %s)
                    ON CONFLICT(source_url)
                    DO UPDATE SET
                        content_hash = EXCLUDED.content_hash,
                        status = EXCLUDED.status,
                        message = EXCLUDED.message,
                        last_crawled_at = NOW()
                    """,
                    (url, content_hash, "success", "Indexed successfully"),
                )

def crawl_and_index(url: str):
    title, text = fetch_official_page(url)
    content_hash = hash_text(text)

    if already_crawled_unchanged(url, content_hash):
        return{
            "status": "skipepd",
            "reason": "content unchanged",
            "url": url,
        }

    chunks = chunk_text(text)
    store_chunks(url, title, chunks, content_hash)

    return{
        "status": "indexed",
        "url": url,
        "title": title,
        "chunks": len(chunks)
    }

def search_knowledge(query: str, limit: int = 5):
    query_embedding = model.encode([query])[0].tolist()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    source_url,
                    source_title,
                    chunk_text,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM knowledge
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (query_embedding, query_embedding, limit),
            )
            rows = cur.fetchall()

    return [
        {
            "source_url": row[0],
            "source_title": row[1],
            "chunk_text": row[2],
            "similarity": float(row[3]),
        }
        for row in rows
    ]
