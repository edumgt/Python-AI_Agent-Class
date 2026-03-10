from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project004")
    project_name: str = os.getenv("PROJECT_NAME", "Prj_PersonaVoiceAI")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-1")
    project_topic: str = os.getenv("PROJECT_TOPIC", "개인 맞춤 코칭 음성봇 PERSONA AI 만들기 · 단계 4/5 실전 검증")


settings = Settings()
