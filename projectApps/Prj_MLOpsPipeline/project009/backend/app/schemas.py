from __future__ import annotations

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    values: list[float] = Field(default_factory=lambda: [0.2, 0.4, 0.6])
    note: str = "manual-run"


class RunResponse(BaseModel):
    project_id: str
    status: str
    summary: dict
    history_count: int
