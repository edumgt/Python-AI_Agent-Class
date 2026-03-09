from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.rag_engine import RepoRAG


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RagValidationQueue:
    """Store flagged RAG answers and process them on next reindex."""

    def __init__(self, db_path: Path) -> None:
        base_dir = db_path / "rag_validation"
        base_dir.mkdir(parents=True, exist_ok=True)
        self._base_dir = base_dir
        self._pending_file = base_dir / "pending.json"
        self._runs_dir = base_dir / "runs"
        self._runs_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def pending_count(self) -> int:
        with self._lock:
            return len(self._read_pending())

    def enqueue(self, payload: dict[str, Any]) -> tuple[str, int]:
        with self._lock:
            pending = self._read_pending()
            review_id = uuid.uuid4().hex[:12]
            item = {
                "id": review_id,
                "created_at": _utc_now(),
                "question": str(payload.get("question", "")).strip(),
                "answer": str(payload.get("answer", "")).strip(),
                "sources": self._normalize_sources(payload.get("sources", [])),
                "mode": str(payload.get("mode", "rag")).strip() or "rag",
                "matched_subject": payload.get("matched_subject"),
                "matched_class_id": payload.get("matched_class_id"),
                "note": str(payload.get("note", "")).strip(),
                "top_k": int(payload.get("top_k", 6) or 6),
                "use_llm": payload.get("use_llm"),
            }
            pending.append(item)
            self._write_pending(pending)
            return review_id, len(pending)

    def process_on_reindex(self, rag: RepoRAG) -> dict[str, Any]:
        with self._lock:
            pending = self._read_pending()
            if not pending:
                return {"processed": 0, "report_path": None}

            run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            report_items: list[dict[str, Any]] = []
            for item in pending:
                question = str(item.get("question", "")).strip()
                top_k = int(item.get("top_k", 6) or 6)
                top_k = min(20, max(1, top_k))
                fresh_sources: list[dict[str, Any]] = []
                error = None
                if question:
                    try:
                        fresh_sources = rag.query(question=question, top_k=top_k)
                    except Exception as exc:  # pragma: no cover - defensive logging payload
                        error = str(exc)

                report_items.append(
                    {
                        "id": item.get("id"),
                        "created_at": item.get("created_at"),
                        "processed_at": _utc_now(),
                        "question": question,
                        "previous_answer": item.get("answer", ""),
                        "previous_sources": item.get("sources", []),
                        "fresh_sources": self._normalize_sources(fresh_sources),
                        "mode": item.get("mode", "rag"),
                        "matched_subject": item.get("matched_subject"),
                        "matched_class_id": item.get("matched_class_id"),
                        "note": item.get("note", ""),
                        "error": error,
                    }
                )

            report_payload = {
                "run_id": run_id,
                "generated_at": _utc_now(),
                "processed_count": len(report_items),
                "items": report_items,
            }
            report_path = self._runs_dir / f"{run_id}.json"
            report_path.write_text(
                json.dumps(report_payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            self._write_pending([])
            return {"processed": len(report_items), "report_path": str(report_path)}

    def _normalize_sources(self, raw_sources: Any) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        if not isinstance(raw_sources, list):
            return normalized
        for src in raw_sources[:20]:
            if not isinstance(src, dict):
                continue
            normalized.append(
                {
                    "path": str(src.get("path", "")),
                    "score": float(src.get("score", 0.0)),
                    "chunk": str(src.get("chunk", "")),
                }
            )
        return normalized

    def _read_pending(self) -> list[dict[str, Any]]:
        if not self._pending_file.exists():
            return []
        try:
            data = json.loads(self._pending_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        if not isinstance(data, list):
            return []
        return [item for item in data if isinstance(item, dict)]

    def _write_pending(self, pending: list[dict[str, Any]]) -> None:
        tmp = self._pending_file.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(pending, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp.replace(self._pending_file)
