from __future__ import annotations

from pydantic import BaseModel, Field


class VoiceProfileCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=40)
    language: str = Field("ko")
    base_voice: str = Field("warm_female")
    speaking_rate: float = Field(1.0, ge=0.7, le=1.4)
    pitch_shift: float = Field(0.0, ge=-5.0, le=5.0)
    style_tags: list[str] = Field(default_factory=list)


class VoiceProfileResponse(BaseModel):
    profile_id: str
    name: str
    language: str
    base_voice: str
    speaking_rate: float
    pitch_shift: float
    style_tags: list[str]
    created_at: str


class TrainVoiceRequest(BaseModel):
    profile_id: str = Field(..., min_length=8)
    recordings_count: int = Field(..., ge=10, le=5000)
    total_minutes: float = Field(..., ge=5.0, le=500.0)
    noise_level: float = Field(..., ge=0.0, le=1.0)
    pronunciation_score: float = Field(..., ge=0.0, le=1.0)
    emotion_score: float = Field(..., ge=0.0, le=1.0)
    note: str = Field("train-run", max_length=200)


class TrainVoiceResponse(BaseModel):
    profile_id: str
    status: str
    quality_score: float
    recommendation: str


class SynthesizeRequest(BaseModel):
    profile_id: str = Field(..., min_length=8)
    text: str = Field(..., min_length=1, max_length=400)
    style_strength: float = Field(0.6, ge=0.0, le=1.0)


class SynthesizeResponse(BaseModel):
    profile_id: str
    provider: str
    preview_text: str
    ssml_preview: str


class HistoryItem(BaseModel):
    timestamp: str
    action: str
    payload: dict


class HistoryResponse(BaseModel):
    count: int
    items: list[HistoryItem]
