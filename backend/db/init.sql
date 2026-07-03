CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS knowledge (
    id BIGSERIAL PRIMARY KEY,
    source_url TEXT NOT NULL,
    source_title TEXT,
    chunk_index INT NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL,
    content_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (source_url, chunk_index)
);

CREATE TABLE IF NOT EXISTS crawler_logs (
    id BIGSERIAL PRIMARY KEY,
    source_url TEXT UNIQUE NOT NULL,
    content_hash TEXT NOT NULL,
    last_crawled_at TIMESTAMPTZ DEFAULT NOW(),
    status TEXT NOT NULL,
    message TEXT
);

CREATE INDEX IF NOT EXISTS knowledge_embedding_idx
ON knowledge
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);