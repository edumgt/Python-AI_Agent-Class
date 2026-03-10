from __future__ import annotations

from pydantic import BaseModel, Field


class PersonaUpsertRequest(BaseModel):
    persona_id: str | None = None
    name: str = Field(..., min_length=2, max_length=40)
    role: str = Field("학습 코치", max_length=80)
    tone: str = Field("친절하고 명확한")
    speaking_rules: list[str] = Field(default_factory=list)
    forbidden_topics: list[str] = Field(default_factory=list)
    greeting: str = Field("안녕하세요. 오늘 목표를 함께 정리해볼게요.")


class PersonaResponse(BaseModel):
    persona_id: str
    name: str
    role: str
    tone: str
    speaking_rules: list[str]
    forbidden_topics: list[str]
    greeting: str
    updated_at: str


class PersonaAnswerRequest(BaseModel):
    persona_id: str = Field(..., min_length=4)
    question: str = Field(..., min_length=2, max_length=800)
    context: str = Field("", max_length=1500)
    use_llm: bool = True


class PersonaAnswerResponse(BaseModel):
    persona_id: str
    provider: str
    answer: str
    prompt_preview: str


class HistoryItem(BaseModel):
    timestamp: str
    action: str
    payload: dict


class HistoryResponse(BaseModel):
    count: int
    items: list[HistoryItem]
