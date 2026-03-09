from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project011")
    project_name: str = os.getenv("PROJECT_NAME", "Prj_LLMOpsRAGQuality")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-3")
    project_topic: str = os.getenv("PROJECT_TOPIC", "LLMOps/RAG 서비스 품질관리 · 단계 1/5 입문 이해")


settings = Settings()
