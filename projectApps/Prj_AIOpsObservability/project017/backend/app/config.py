from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project017")
    project_name: str = os.getenv("PROJECT_NAME", "Prj_AIOpsObservability")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-4")
    project_topic: str = os.getenv("PROJECT_TOPIC", "AIOps 관측성·이상탐지·자동복구 · 단계 2/5 기초 구현")


settings = Settings()
