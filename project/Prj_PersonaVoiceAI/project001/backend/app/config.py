from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project001")
    project_name: str = os.getenv("PROJECT_NAME", "나만의 음성 모델 만들기")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-A")
    project_topic: str = os.getenv("PROJECT_TOPIC", "나만의 음성 모델 만들기")
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data")).resolve()


settings = Settings()
