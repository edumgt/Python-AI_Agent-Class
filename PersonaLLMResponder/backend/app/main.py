from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.core import (
    answer_with_openai,
    answer_without_llm,
    append_history,
    build_prompt,
    get_persona,
    list_personas,
    load_recent,
    upsert_persona,
)
from backend.app.schemas import (
    HistoryResponse,
    PersonaAnswerRequest,
    PersonaAnswerResponse,
    PersonaResponse,
    PersonaUpsertRequest,
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
PERSONAS_FILE = DATA_DIR / "personas.json"
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
        "personas": len(list_personas(PERSONAS_FILE)),
        "openai_enabled": bool(settings.openai_api_key),
    }


@app.get("/v1/project/meta")
def project_meta() -> dict:
    return {
        "project_id": settings.project_id,
        "project_name": settings.project_name,
        "track": settings.project_track,
        "topic": settings.project_topic,
    }


@app.get("/v1/persona/list", response_model=list[PersonaResponse])
def persona_list() -> list[PersonaResponse]:
    return [PersonaResponse(**row) for row in list_personas(PERSONAS_FILE)]


@app.post("/v1/persona/upsert", response_model=PersonaResponse)
def persona_upsert(payload: PersonaUpsertRequest) -> PersonaResponse:
    record = upsert_persona(PERSONAS_FILE, payload.model_dump())
    append_history(HISTORY_FILE, "upsert_persona", record)
    return PersonaResponse(**record)


@app.post("/v1/persona/answer", response_model=PersonaAnswerResponse)
def persona_answer(payload: PersonaAnswerRequest) -> PersonaAnswerResponse:
    persona = get_persona(PERSONAS_FILE, payload.persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="persona not found")

    prompt = build_prompt(persona=persona, question=payload.question, context=payload.context)

    text: str | None = None
    provider = "local-rule"
    if payload.use_llm:
        text = answer_with_openai(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            prompt=prompt,
            persona=persona,
        )
        if text:
            provider = "openai"

    if not text:
        text = answer_without_llm(persona=persona, question=payload.question, context=payload.context)

    result = {
        "persona_id": persona["persona_id"],
        "provider": provider,
        "answer": text,
        "prompt_preview": prompt[:400],
    }
    append_history(HISTORY_FILE, "persona_answer", {"input": payload.model_dump(), "result": result})
    return PersonaAnswerResponse(**result)


@app.get("/v1/project/history", response_model=HistoryResponse)
def project_history(limit: int = 20) -> HistoryResponse:
    items = load_recent(HISTORY_FILE, limit=max(1, min(200, limit)))
    return HistoryResponse(count=len(items), items=items)
