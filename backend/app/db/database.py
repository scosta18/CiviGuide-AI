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
    id          BIGSERIAL PRIMARY KEY,
    url         TEXT NOT NULL,          -- official page this chunk came from
    title       TEXT,                   -- human-readable page title
    program     TEXT DEFAULT 'MD_SNAP', -- which benefit program (MVP: one)
    source_hash TEXT,                   -- sha256 of the page, for change detection
    content     TEXT NOT NULL,          -- the chunk text itself
    embedding   VECTOR(1536),           -- must match EMBEDDING_DIM in config
    last_seen   TIMESTAMPTZ DEFAULT now()
);

-- Audit log of crawler runs: proves data freshness, feeds an admin view later.
CREATE TABLE IF NOT EXISTS crawler_logs (
    id      BIGSERIAL PRIMARY KEY,
    url     TEXT NOT NULL,
    status  TEXT NOT NULL,              -- 'ok' | 'changed' | 'error' | 'skipped'
    detail  TEXT,
    ran_at  TIMESTAMPTZ DEFAULT now()
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
