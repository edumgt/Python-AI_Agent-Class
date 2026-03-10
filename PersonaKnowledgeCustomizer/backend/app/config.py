from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass
class Settings:
    project_id: str = os.getenv("PROJECT_ID", "project003")
    project_name: str = os.getenv("PROJECT_NAME", "사전 데이터 기반 PERSO AI의 답변 커스텀하기")
    project_track: str = os.getenv("PROJECT_TRACK", "프로젝트-C")
    project_topic: str = os.getenv("PROJECT_TOPIC", "사전 데이터 기반 PERSO AI의 답변 커스텀하기")
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data")).resolve()


settings = Settings()
