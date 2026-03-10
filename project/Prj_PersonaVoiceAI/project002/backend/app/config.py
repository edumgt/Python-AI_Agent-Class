from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project002")
    project_name: str = os.getenv("PROJECT_NAME", "거대 언어 모델을 활용한 PERSONA AI 답변 기능 구현하기")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-B")
    project_topic: str = os.getenv("PROJECT_TOPIC", "거대 언어 모델을 활용한 PERSONA AI 답변 기능 구현하기")
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data")).resolve()

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


settings = Settings()
