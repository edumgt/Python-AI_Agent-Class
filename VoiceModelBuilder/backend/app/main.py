from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.core import (
    append_history,
    create_profile,
    get_profile,
    list_profiles,
    load_recent,
    synthesize_preview,
    train_profile,
)
from backend.app.schemas import (
    HistoryResponse,
    SynthesizeRequest,
    SynthesizeResponse,
    TrainVoiceRequest,
    TrainVoiceResponse,
    VoiceProfileCreateRequest,
    VoiceProfileResponse,
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
PROFILES_FILE = DATA_DIR / "voice_profiles.json"
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
        "profiles": len(list_profiles(PROFILES_FILE)),
        "history_count": len(load_recent(HISTORY_FILE, limit=1000)),
    }


@app.get("/v1/project/meta")
def project_meta() -> dict:
    return {
        "project_id": settings.project_id,
        "project_name": settings.project_name,
        "track": settings.project_track,
        "topic": settings.project_topic,
    }


@app.post("/v1/voice/profiles", response_model=VoiceProfileResponse)
def create_voice_profile(payload: VoiceProfileCreateRequest) -> VoiceProfileResponse:
    profile = create_profile(PROFILES_FILE, payload.model_dump())
    append_history(HISTORY_FILE, "create_profile", profile)
    return VoiceProfileResponse(**profile)


@app.get("/v1/voice/profiles", response_model=list[VoiceProfileResponse])
def list_voice_profiles() -> list[VoiceProfileResponse]:
    return [VoiceProfileResponse(**row) for row in list_profiles(PROFILES_FILE)]


@app.post("/v1/voice/train", response_model=TrainVoiceResponse)
def train_voice(payload: TrainVoiceRequest) -> TrainVoiceResponse:
    profile = get_profile(PROFILES_FILE, payload.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="profile not found")

    result = train_profile(profile=profile, payload=payload.model_dump())
    append_history(HISTORY_FILE, "train_voice", {"input": payload.model_dump(), "result": result})
    return TrainVoiceResponse(**result)


@app.post("/v1/voice/synthesize", response_model=SynthesizeResponse)
def synthesize_voice(payload: SynthesizeRequest) -> SynthesizeResponse:
    profile = get_profile(PROFILES_FILE, payload.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="profile not found")

    result = synthesize_preview(profile=profile, text=payload.text, style_strength=payload.style_strength)
    append_history(HISTORY_FILE, "synthesize_preview", {"input": payload.model_dump(), "result": result})
    return SynthesizeResponse(**result)


@app.get("/v1/project/history", response_model=HistoryResponse)
def project_history(limit: int = 20) -> HistoryResponse:
    items = load_recent(HISTORY_FILE, limit=max(1, min(200, limit)))
    return HistoryResponse(count=len(items), items=items)
