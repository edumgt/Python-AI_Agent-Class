from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project004")
    project_name: str = os.getenv("PROJECT_NAME", "Prj_DevOpsKickoff")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-1")
    project_topic: str = os.getenv("PROJECT_TOPIC", "DevOps 프로젝트 착수와 요구사항 정의 · 단계 4/5 실전 검증")


settings = Settings()
