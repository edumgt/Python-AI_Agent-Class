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
        profile_score = max(0.0, min(100.0, round(avg * 100, 2)))
        style_consistency = max(0.0, min(100.0, round((1.0 - std) * 100, 2)))
        status = "ready" if profile_score >= 70 else "design"
        summary = {
            "phase": "개인 맞춤 코칭 음성봇 기초 구축",
            "profile_score": profile_score,
            "style_consistency": style_consistency,
            "note": note,
        }
    elif track_code == "프로젝트-2":
        loop_quality = max(0.0, min(100.0, round((avg - std * 0.4) * 100, 2)))
        status = "stable" if loop_quality >= 68 else "tune"
        summary = {
            "phase": "STT-LLM-TTS 코칭 대화 파이프라인",
            "loop_quality": loop_quality,
            "latency_hint_ms": int((0.18 + std) * 1000),
            "note": note,
        }
    elif track_code == "프로젝트-3":
        dataset_quality = max(0.0, min(100.0, round((avg * 0.7 + (1.0 - std) * 0.3) * 100, 2)))
        status = "usable" if dataset_quality >= 72 else "relabel"
        summary = {
            "phase": "사전 데이터 기반 PERSONA AI 구축",
            "dataset_quality": dataset_quality,
            "label_consistency": round((1.0 - std) * 100, 2),
            "note": note,
        }
    else:
        drift_score = max(0.0, min(100.0, round(((1.0 - avg) + std) * 100, 2)))
        status = "retrain" if drift_score >= 35 else "monitor"
        summary = {
            "phase": "PERSONA AI 지속학습과 품질 운영",
            "drift_score": drift_score,
            "next_action": "재학습 큐 등록" if status == "retrain" else "모니터링 유지",
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
