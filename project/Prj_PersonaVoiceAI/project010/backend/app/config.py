from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project010")
    project_name: str = os.getenv("PROJECT_NAME", "Prj_PersonaVoiceAI")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-2")
    project_topic: str = os.getenv("PROJECT_TOPIC", "PERSONA 코칭 대화 파이프라인(STT↔LLM↔TTS) · 단계 5/5 운영 최적화")


settings = Settings()
