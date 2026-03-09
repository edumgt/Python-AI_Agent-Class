from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project010")
    project_name: str = os.getenv("PROJECT_NAME", "Prj_MLOpsPipeline")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-2")
    project_topic: str = os.getenv("PROJECT_TOPIC", "MLOps 파이프라인과 모델 레지스트리 · 단계 5/5 운영 최적화")


settings = Settings()
