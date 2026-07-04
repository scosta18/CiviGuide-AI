import time
import psycopg

from app.core.config import get_database_url

# SQL to set up everything the MVP needs. Runs on every app startup;
# 'IF NOT EXISTS' makes it safe to run repeatedly (idempotent).
SCHEMA_SQL = """
-- pgvector extension gives Postgres the VECTOR column type + similarity ops.
CREATE EXTENSION IF NOT EXISTS vector;

-- The knowledge base: chunks of official-source text with their embeddings.
CREATE TABLE IF NOT EXISTS knowledge (
    id            BIGSERIAL PRIMARY KEY,
    source_url    TEXT NOT NULL,
    source_title  TEXT,
    chunk_index   INT NOT NULL,
    chunk_text    TEXT NOT NULL,
    embedding     VECTOR(384),
    content_hash  TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT now(),
    UNIQUE (source_url, chunk_index)
);

CREATE TABLE IF NOT EXISTS crawler_logs (
    id              BIGSERIAL PRIMARY KEY,
    source_url      TEXT UNIQUE NOT NULL,
    content_hash    TEXT NOT NULL,
    last_crawled_at TIMESTAMPTZ DEFAULT now(),
    status          TEXT NOT NULL,
    message         TEXT
);
"""


def get_connection() -> psycopg.Connection:
    """Open a new database connection using the configured URL."""
    return psycopg.connect(get_database_url())


def init_schema(retries: int = 10, delay_seconds: float = 2.0) -> None:
    """
    Create the extension and tables if they don't exist yet.

    Retries because Postgres inside Docker takes a few seconds to accept
    connections after the container starts (depends_on doesn't wait for
    readiness, only for container start).
    """
    for attempt in range(1, retries + 1):
        try:
            with get_connection() as conn:
                conn.execute(SCHEMA_SQL)
            return  # success — stop retrying
        except Exception:
            if attempt == retries:
                raise  # out of retries — let the app crash loudly
            time.sleep(delay_seconds)
