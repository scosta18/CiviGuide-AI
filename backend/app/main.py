from fastapi import FastAPI

app = FastAPI(title="CiviGuide-AI")

@app.get("/api/health")
def health():
    return {"status": "ok"}