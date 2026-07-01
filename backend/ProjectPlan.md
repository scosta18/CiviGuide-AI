<<<<<<< HEAD
# CiviGuide-AI — Project Plan

## Project Description

An AI-powered multi-agent platform that helps people discover, understand, and
apply for government benefits using verified information from official sources.

For the MVP, scope is deliberately narrowed to **one program: Maryland SNAP
(food assistance)**. Everything is built to prove one core loop end-to-end before
expanding to other programs.

## Purpose

Government benefit information is scattered, hard to read, and easy to get wrong.
CiviGuide-AI gives people plain-language answers about SNAP eligibility, grounded
**only in official sources**, with a citation on every answer so users can verify
it themselves.

What makes it more than "ChatGPT with a prompt":
- A **graph-based multi-agent workflow** (retrieve, then reason) rather than a single chatbot.
- **Official sources cited** with every recommendation.
- A **fresh knowledge base** kept current by a crawler that detects changes.
- **Production-minded**: containerized, tested, with the legal safety line enforced in code.

## Legal Line (non-negotiable)

CiviGuide-AI provides **general information, not legal advice and not an
eligibility determination.** Only the Maryland Department of Human Services can
determine actual eligibility. This is enforced in code, not just shown in the UI:
no answer is returned without an official citation, and definitive "you qualify"
language is never used.

---

## Resources Needed

Gather these before/while building. Put real secrets in a local `.env` (never commit it).

### API keys / accounts
- **LLM provider key** — OpenAI API key (or an open-weight model via Ollama/vLLM if avoiding cost).
  Used for: generating answers + creating embeddings.
- **GitHub account** — already have (`scosta18/CiviGuide-AI`). For CI/CD later.

### Runtime services (run locally first, no signup needed)
- **PostgreSQL + pgvector** — vector storage for the knowledge base. Local via Docker.
- **Redis** — caching / queue later. Local via Docker.

### Official data sources (the knowledge base — no key needed, just URLs)
- `dhs.maryland.gov` — Maryland SNAP program + eligibility pages
- `fns.usda.gov` — federal SNAP rules
- `marylandsnap.com`, `mdthink.maryland.gov` — official MD portals

### Local tools to install
- **Python 3.12+**
- **Docker Desktop** (for Postgres/Redis, and containerizing later)
- **Node.js 20+** (for the Next.js frontend, added later)

---

## Phases & Steps

### Phase 1 — Skeleton & Environment
1. Create repo structure (`backend/app/`) and `requirements.txt`.
2. Write a minimal FastAPI app with a `/api/health` endpoint.
3. Run it locally in a virtual environment; confirm `/health` returns `{"status": "ok"}`.
4. Add `.gitignore` and `.env.example`.

### Phase 2 — Containerization
1. Write the backend `Dockerfile`.
2. Write `docker-compose.yml` with three services: backend, Postgres (pgvector image), Redis.
3. Boot the stack; confirm the backend container can reach Postgres and Redis.

### Phase 3 — Knowledge Base
1. Define the database schema (`knowledge` table with a `vector` column; `crawler_logs` table).
2. Build the crawler: fetch one official page, **reject any non-allow-listed domain**.
3. Chunk the page text, create embeddings, store chunks + vectors in Postgres.
4. Add change detection (hash the source; skip re-embedding if unchanged).
5. Build vector search: given a query, return the most relevant official chunks.
6. Seed the knowledge base with a handful of official MD SNAP pages.

### Phase 4 — Agents & Orchestration
1. Write the **Retrieval Agent**: wraps vector search, filters out weak matches.
2. Write the **Eligibility Agent**: answers using ONLY retrieved official context.
3. Wire both into a **LangGraph** flow: `retrieve -> reason` (retrieval always runs first).

### Phase 5 — Guardrails & API
1. Write the guardrail module: block any answer with no citation; soften
   "you qualify" -> "you may be eligible"; append the required disclaimer.
2. Add unit tests for the guardrails.
3. Expose a `/api/chat` endpoint: question in, grounded+cited answer out.

### Phase 6 — Frontend
1. Set up Next.js + TypeScript.
2. Build a single chat page: input box, answer display, clickable official sources.
3. Connect it to the `/api/chat` endpoint.

### Phase 7 — Demo & Hardening
1. Run the full loop end-to-end: ask a real SNAP question, get a cited answer.
2. Add basic logging.
3. Write a README with run instructions.

### Phase 8 — Stretch (only after the above works)
- User auth + saved profile (income/household) to reduce repeated questions.
- Planner Agent (step-by-step application checklist).
- Scheduled re-crawl + a read-only admin view of crawler freshness.
- Document upload + OCR (use a cloud OCR, not Tesseract, for real IDs/paystubs).
- Multi-program (Medicaid, TCA), Spanish, metrics/monitoring.

### Explicitly NOT doing (for now)
- Kubernetes — Docker Compose is enough at this scale.
- Making eligibility **determinations** — that's the legal line; never cross it.
=======
# CiviGuide-AI — Project Plan

## Project Description

An AI-powered multi-agent platform that helps people discover, understand, and
apply for government benefits using verified information from official sources.

For the MVP, scope is deliberately narrowed to **one program: Maryland SNAP
(food assistance)**. Everything is built to prove one core loop end-to-end before
expanding to other programs.

## Purpose

Government benefit information is scattered, hard to read, and easy to get wrong.
CiviGuide-AI gives people plain-language answers about SNAP eligibility, grounded
**only in official sources**, with a citation on every answer so users can verify
it themselves.

What makes it more than "ChatGPT with a prompt":
- A **graph-based multi-agent workflow** (retrieve, then reason) rather than a single chatbot.
- **Official sources cited** with every recommendation.
- A **fresh knowledge base** kept current by a crawler that detects changes.
- **Production-minded**: containerized, tested, with the legal safety line enforced in code.

## Legal Line (non-negotiable)

CiviGuide-AI provides **general information, not legal advice and not an
eligibility determination.** Only the Maryland Department of Human Services can
determine actual eligibility. This is enforced in code, not just shown in the UI:
no answer is returned without an official citation, and definitive "you qualify"
language is never used.

---

## Resources Needed

Gather these before/while building. Put real secrets in a local `.env` (never commit it).

### API keys / accounts
- **LLM provider key** — OpenAI API key (or an open-weight model via Ollama/vLLM if avoiding cost).
  Used for: generating answers + creating embeddings.
- **GitHub account** — already have (`scosta18/CiviGuide-AI`). For CI/CD later.

### Runtime services (run locally first, no signup needed)
- **PostgreSQL + pgvector** — vector storage for the knowledge base. Local via Docker.
- **Redis** — caching / queue later. Local via Docker.

### Official data sources (the knowledge base — no key needed, just URLs)
- `dhs.maryland.gov` — Maryland SNAP program + eligibility pages
- `fns.usda.gov` — federal SNAP rules
- `marylandsnap.com`, `mdthink.maryland.gov` — official MD portals

### Local tools to install
- **Python 3.12+**
- **Docker Desktop** (for Postgres/Redis, and containerizing later)
- **Node.js 20+** (for the Next.js frontend, added later)

---

## Phases & Steps

### Phase 1 — Skeleton & Environment
1. Create repo structure (`backend/app/`) and `requirements.txt`.
2. Write a minimal FastAPI app with a `/api/health` endpoint.
3. Run it locally in a virtual environment; confirm `/health` returns `{"status": "ok"}`.
4. Add `.gitignore` and `.env.example`.

### Phase 2 — Containerization
1. Write the backend `Dockerfile`.
2. Write `docker-compose.yml` with three services: backend, Postgres (pgvector image), Redis.
3. Boot the stack; confirm the backend container can reach Postgres and Redis.

### Phase 3 — Knowledge Base
1. Define the database schema (`knowledge` table with a `vector` column; `crawler_logs` table).
2. Build the crawler: fetch one official page, **reject any non-allow-listed domain**.
3. Chunk the page text, create embeddings, store chunks + vectors in Postgres.
4. Add change detection (hash the source; skip re-embedding if unchanged).
5. Build vector search: given a query, return the most relevant official chunks.
6. Seed the knowledge base with a handful of official MD SNAP pages.

### Phase 4 — Agents & Orchestration
1. Write the **Retrieval Agent**: wraps vector search, filters out weak matches.
2. Write the **Eligibility Agent**: answers using ONLY retrieved official context.
3. Wire both into a **LangGraph** flow: `retrieve -> reason` (retrieval always runs first).

### Phase 5 — Guardrails & API
1. Write the guardrail module: block any answer with no citation; soften
   "you qualify" -> "you may be eligible"; append the required disclaimer.
2. Add unit tests for the guardrails.
3. Expose a `/api/chat` endpoint: question in, grounded+cited answer out.

### Phase 6 — Frontend
1. Set up Next.js + TypeScript.
2. Build a single chat page: input box, answer display, clickable official sources.
3. Connect it to the `/api/chat` endpoint.

### Phase 7 — Demo & Hardening
1. Run the full loop end-to-end: ask a real SNAP question, get a cited answer.
2. Add basic logging.
3. Write a README with run instructions.

### Phase 8 — Stretch (only after the above works)
- User auth + saved profile (income/household) to reduce repeated questions.
- Planner Agent (step-by-step application checklist).
- Scheduled re-crawl + a read-only admin view of crawler freshness.
- Document upload + OCR (use a cloud OCR, not Tesseract, for real IDs/paystubs).
- Multi-program (Medicaid, TCA), Spanish, metrics/monitoring.

### Explicitly NOT doing (for now)
- Kubernetes — Docker Compose is enough at this scale.
- Making eligibility **determinations** — that's the legal line; never cross it.
>>>>>>> origin/Moh_dev
