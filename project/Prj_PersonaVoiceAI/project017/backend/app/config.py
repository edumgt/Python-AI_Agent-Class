from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project017")
    project_name: str = os.getenv("PROJECT_NAME", "Prj_PersonaVoiceAI")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-4")
    project_topic: str = os.getenv("PROJECT_TOPIC", "PERSONA AI 지속학습과 품질 운영 · 단계 2/5 기초 구현")


settings = Settings()
