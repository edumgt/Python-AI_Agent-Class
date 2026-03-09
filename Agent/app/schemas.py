from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, description="질문")
    top_k: int = Field(6, ge=1, le=20)
    use_llm: bool = Field(True, description="OPENAI_API_KEY가 있으면 LLM 답변 생성")


class SourceItem(BaseModel):
    path: str
    score: float
    chunk: str


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    mode: str = "rag"
    matched_subject: str | None = None
    matched_class_id: str | None = None


class ReindexResponse(BaseModel):
    indexed_files: int
    indexed_chunks: int
    collection: str


class RagValidationQueueRequest(BaseModel):
    question: str = Field(..., min_length=2, description="검증이 필요한 질문")
    answer: str = Field("", description="사용자에게 제공된 기존 답변")
    sources: List[SourceItem] = Field(default_factory=list)
    mode: str = Field("rag")
    matched_subject: str | None = None
    matched_class_id: str | None = None
    note: str = Field("", max_length=500)
    top_k: int = Field(6, ge=1, le=20)
    use_llm: bool | None = None


class RagValidationQueueResponse(BaseModel):
    review_id: str
    pending_count: int


class RagValidationPendingResponse(BaseModel):
    pending_count: int
