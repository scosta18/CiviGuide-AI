from fastapi import FastAPI
import os
import psycopg
import redis

app = FastAPI()


@app.get("/api/health")
def health():

    db = "down"
    cache = "down"

    try:
        conn = psycopg.connect(os.getenv("DATABASE_URL"))
        conn.close()
        db = "up"
    except Exception:
        pass

    try:
        r = redis.from_url(os.getenv("REDIS_URL"))
        r.ping()
        cache = "up"
    except Exception:
        pass

    return {
        "status": "ok",
        "postgres": db,
        "redis": cache
    }
