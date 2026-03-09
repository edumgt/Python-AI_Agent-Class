from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import statistics


@dataclass
class ScenarioResult:
    track: str
    status: str
    summary: dict


def _safe_mean(values: list[float]) -> float:
    return float(statistics.fmean(values)) if values else 0.0


def _safe_stdev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return float(statistics.pstdev(values))


def evaluate(track_code: str, values: list[float], note: str) -> ScenarioResult:
    values = [float(v) for v in values]
    avg = _safe_mean(values)
    std = _safe_stdev(values)

    if track_code == "프로젝트-1":
        # DevOps kickoff: readiness gate
        readiness = max(0.0, min(100.0, round((1.0 - avg) * 100, 2)))
        status = "go" if readiness >= 60 else "hold"
        summary = {
            "readiness_score": readiness,
            "gate": "deployment-readiness",
            "risk_mean": round(avg, 4),
            "note": note,
        }
    elif track_code == "프로젝트-2":
        # MLOps pipeline: model quality stability
        quality = max(0.0, min(100.0, round(avg * 100, 2)))
        status = "stable" if std <= 0.12 else "unstable"
        summary = {
            "quality_score": quality,
            "drift_std": round(std, 4),
            "pipeline_state": status,
            "note": note,
        }
    elif track_code == "프로젝트-3":
        # LLMOps/RAG: answer quality guardrail
        grounded = max(0.0, min(100.0, round(avg * 100, 2)))
        status = "pass" if grounded >= 70 else "review"
        summary = {
            "groundedness": grounded,
            "guardrail": status,
            "signal_std": round(std, 4),
            "note": note,
        }
    else:
        # AIOps: anomaly monitoring
        anomaly_score = max(0.0, min(100.0, round((avg + std) * 100, 2)))
        status = "alert" if anomaly_score >= 65 else "normal"
        summary = {
            "anomaly_score": anomaly_score,
            "status": status,
            "baseline_std": round(std, 4),
            "note": note,
        }

    return ScenarioResult(track=track_code, status=status, summary=summary)


def append_history(history_file: Path, payload: dict) -> None:
    history_file.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    with history_file.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_recent(history_file: Path, limit: int = 20) -> list[dict]:
    if not history_file.exists():
        return []
    lines = history_file.read_text(encoding="utf-8").splitlines()
    rows = []
    for line in lines[-max(1, limit):]:
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows
