from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.core import append_history, evaluate, load_recent
from backend.app.schemas import RunRequest, RunResponse


app = FastAPI(title=f"{settings.project_id} API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"
HISTORY_FILE = DATA_DIR / "run_history.jsonl"

if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")


@app.get("/")
def home() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health() -> dict:
    recent = load_recent(HISTORY_FILE, limit=1)
    return {
        "status": "ok",
        "project_id": settings.project_id,
        "project_name": settings.project_name,
        "track": settings.project_track,
        "topic": settings.project_topic,
        "history_exists": bool(recent),
    }


@app.get("/v1/project/meta")
def project_meta() -> dict:
    return {
        "project_id": settings.project_id,
        "project_name": settings.project_name,
        "track": settings.project_track,
        "topic": settings.project_topic,
    }


@app.get("/v1/project/history")
def project_history(limit: int = 20) -> dict:
    rows = load_recent(HISTORY_FILE, limit=limit)
    return {"items": rows, "count": len(rows)}


@app.post("/v1/project/run", response_model=RunResponse)
def project_run(payload: RunRequest) -> RunResponse:
    result = evaluate(
        track_code=settings.project_track,
        values=payload.values,
        note=payload.note,
    )
    record = {
        "project_id": settings.project_id,
        "project_name": settings.project_name,
        "track": result.track,
        "status": result.status,
        "summary": result.summary,
    }
    append_history(HISTORY_FILE, record)
    history_count = len(load_recent(HISTORY_FILE, limit=10_000))
    return RunResponse(
        project_id=settings.project_id,
        status=result.status,
        summary=result.summary,
        history_count=history_count,
    )
