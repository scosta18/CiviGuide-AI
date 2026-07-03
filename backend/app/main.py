from fastapi import FastAPI
import os
import psycopg
import redis


from pydantic import BaseModel

from app.kb import crawl_and_index, search_knowledge


app = FastAPI()


class CrawlRequest(BaseModel):
    url: str


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/kb/crawl")
def crawl_page(request: CrawlRequest):
    return crawl_and_index(request.url)


@app.post("/api/kb/search")
def search_kb(request: SearchRequest):
    return {
        "query": request.query,
        "results": search_knowledge(request.query, request.limit),
    }