from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.core import (
    append_history,
    bootstrap_knowledge,
    build_custom_answer,
    list_knowledge,
    load_recent,
    retrieve_knowledge,
    upsert_knowledge,
)
from backend.app.schemas import (
    CustomAnswerRequest,
    CustomAnswerResponse,
    HistoryResponse,
    KnowledgeItemResponse,
    KnowledgeUpsertRequest,
    MatchedKnowledge,
)

app = FastAPI(title=f"{settings.project_id} API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = settings.data_dir if str(settings.data_dir).startswith("/") else PROJECT_ROOT / "data"
KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"
HISTORY_FILE = DATA_DIR / "run_history.jsonl"

if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")


@app.get("/")
def home() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "project_id": settings.project_id,
        "project_name": settings.project_name,
        "topic": settings.project_topic,
        "knowledge_items": len(list_knowledge(KNOWLEDGE_FILE)),
    }


@app.get("/v1/project/meta")
def project_meta() -> dict:
    return {
        "project_id": settings.project_id,
        "project_name": settings.project_name,
        "track": settings.project_track,
        "topic": settings.project_topic,
    }


@app.post("/v1/knowledge/upsert", response_model=list[KnowledgeItemResponse])
def knowledge_upsert(payload: KnowledgeUpsertRequest) -> list[KnowledgeItemResponse]:
    rows = upsert_knowledge(KNOWLEDGE_FILE, [item.model_dump() for item in payload.items])
    append_history(HISTORY_FILE, "knowledge_upsert", {"count": len(rows)})
    return [KnowledgeItemResponse(**row) for row in rows]


@app.post("/v1/knowledge/bootstrap", response_model=list[KnowledgeItemResponse])
def knowledge_bootstrap() -> list[KnowledgeItemResponse]:
    rows = bootstrap_knowledge(KNOWLEDGE_FILE)
    append_history(HISTORY_FILE, "knowledge_bootstrap", {"count": len(rows)})
    return [KnowledgeItemResponse(**row) for row in rows]


@app.get("/v1/knowledge/list", response_model=list[KnowledgeItemResponse])
def knowledge_list() -> list[KnowledgeItemResponse]:
    return [KnowledgeItemResponse(**row) for row in list_knowledge(KNOWLEDGE_FILE)]


@app.post("/v1/custom/answer", response_model=CustomAnswerResponse)
def custom_answer(payload: CustomAnswerRequest) -> CustomAnswerResponse:
    matched = retrieve_knowledge(KNOWLEDGE_FILE, payload.question, payload.top_k)
    answer = build_custom_answer(
        persona_name=payload.persona_name,
        style=payload.style,
        question=payload.question,
        matched=matched,
    )

    result = {
        "answer": answer,
        "matched": [
            {
                "item_id": row["item_id"],
                "title": row["title"],
                "score": row["score"],
            }
            for row in matched
        ],
    }
    append_history(HISTORY_FILE, "custom_answer", {"input": payload.model_dump(), "matched": result["matched"]})

    return CustomAnswerResponse(
        answer=result["answer"],
        matched=[MatchedKnowledge(**row) for row in result["matched"]],
    )


@app.get("/v1/project/history", response_model=HistoryResponse)
def project_history(limit: int = 20) -> HistoryResponse:
    items = load_recent(HISTORY_FILE, limit=max(1, min(200, limit)))
    return HistoryResponse(count=len(items), items=items)
