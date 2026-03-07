from __future__ import annotations

import os
from pathlib import Path


class Settings:
    def __init__(self) -> None:
        self.repo_root = Path(os.getenv("REPO_ROOT", "/srv/repo")).resolve()
        self.vector_db_path = Path(os.getenv("VECTOR_DB_PATH", "/srv/vector_db")).resolve()
        self.vector_collection = os.getenv("VECTOR_COLLECTION", "curriculum_repo")
        self.embedding_dim = int(os.getenv("EMBEDDING_DIM", "1024"))
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "900"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "150"))
        self.default_top_k = int(os.getenv("DEFAULT_TOP_K", "6"))
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


settings = Settings()
