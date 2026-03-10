from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class TraceLogger:
    def __init__(self, *, langsmith_enabled: bool, langsmith_api_key: str, langsmith_project: str) -> None:
        self._logger = logging.getLogger("agent.telemetry")
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(message)s"))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

        self._langsmith_enabled = bool(langsmith_enabled)
        self._langsmith_project = langsmith_project
        self._langsmith_client = None

        if self._langsmith_enabled and langsmith_api_key:
            try:
                from langsmith import Client  # type: ignore

                self._langsmith_client = Client(api_key=langsmith_api_key)
            except Exception:
                self._langsmith_client = None

    @property
    def langsmith_ready(self) -> bool:
        return self._langsmith_client is not None

    def log_event(
        self,
        *,
        event: str,
        inputs: dict[str, Any],
        outputs: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        user_id: str | None = None,
        enable_langsmith: bool | None = None,
    ) -> str:
        trace_id = f"trace_{uuid.uuid4().hex[:20]}"
        record = {
            "trace_id": trace_id,
            "timestamp": _utc_now_iso(),
            "event": event,
            "user_id": user_id,
            "inputs": self._safe_json(inputs),
            "outputs": self._safe_json(outputs or {}),
            "metadata": self._safe_json(metadata or {}),
        }
        self._logger.info(json.dumps(record, ensure_ascii=False))

        use_langsmith = self._langsmith_enabled if enable_langsmith is None else bool(enable_langsmith)
        if use_langsmith and self._langsmith_client is not None:
            self._send_langsmith(record)

        return trace_id

    def _send_langsmith(self, record: dict[str, Any]) -> None:
        try:
            self._langsmith_client.create_run(  # type: ignore[union-attr]
                name=str(record.get("event", "agent_event")),
                run_type="chain",
                inputs=record.get("inputs", {}),
                outputs=record.get("outputs", {}),
                extra={
                    "metadata": {
                        "trace_id": record.get("trace_id"),
                        "user_id": record.get("user_id"),
                        **(record.get("metadata") or {}),
                    }
                },
                project_name=self._langsmith_project,
            )
        except Exception:
            # LangSmith 전송 실패가 API 기능 자체를 막지 않도록 무시한다.
            return

    @staticmethod
    def _safe_json(value: Any) -> Any:
        try:
            json.dumps(value, ensure_ascii=False)
            return value
        except TypeError:
            return str(value)
