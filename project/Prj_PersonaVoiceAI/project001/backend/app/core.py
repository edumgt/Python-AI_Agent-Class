from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import uuid


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(path: Path, default: list[dict]) -> list[dict]:
    if not path.exists():
        return list(default)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return list(default)
    if not isinstance(raw, list):
        return list(default)
    return [row for row in raw if isinstance(row, dict)]


def _save_json(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def append_history(history_file: Path, action: str, payload: dict) -> None:
    history_file.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "timestamp": _now_iso(),
        "action": action,
        "payload": payload,
    }
    with history_file.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_recent(history_file: Path, limit: int = 30) -> list[dict]:
    if not history_file.exists():
        return []
    rows: list[dict] = []
    for line in history_file.read_text(encoding="utf-8").splitlines()[-max(1, limit):]:
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            rows.append(item)
    return rows


def create_profile(profiles_file: Path, payload: dict) -> dict:
    profiles = _load_json(profiles_file, default=[])
    profile = {
        "profile_id": f"vp_{uuid.uuid4().hex[:12]}",
        "name": str(payload.get("name", "")).strip(),
        "language": str(payload.get("language", "ko")).strip(),
        "base_voice": str(payload.get("base_voice", "warm_female")).strip(),
        "speaking_rate": float(payload.get("speaking_rate", 1.0)),
        "pitch_shift": float(payload.get("pitch_shift", 0.0)),
        "style_tags": [str(tag).strip() for tag in payload.get("style_tags", []) if str(tag).strip()],
        "created_at": _now_iso(),
    }
    profiles.append(profile)
    _save_json(profiles_file, profiles)
    return profile


def list_profiles(profiles_file: Path) -> list[dict]:
    profiles = _load_json(profiles_file, default=[])
    profiles.sort(key=lambda row: str(row.get("created_at", "")), reverse=True)
    return profiles


def get_profile(profiles_file: Path, profile_id: str) -> dict | None:
    for row in _load_json(profiles_file, default=[]):
        if str(row.get("profile_id", "")) == profile_id:
            return row
    return None


def train_profile(profile: dict, payload: dict) -> dict:
    recordings_count = int(payload.get("recordings_count", 0))
    total_minutes = float(payload.get("total_minutes", 0.0))
    noise_level = float(payload.get("noise_level", 0.0))
    pronunciation_score = float(payload.get("pronunciation_score", 0.0))
    emotion_score = float(payload.get("emotion_score", 0.0))

    coverage_score = min(100.0, (recordings_count * 0.9) + (total_minutes * 0.55))
    pronunciation_bonus = pronunciation_score * 22.0
    emotion_bonus = emotion_score * 14.0
    noise_penalty = noise_level * 35.0

    quality = max(0.0, min(100.0, coverage_score + pronunciation_bonus + emotion_bonus - noise_penalty))
    quality = round(quality, 2)

    if quality >= 78:
        status = "ready"
        recommendation = "상용 배포 전 문장 길이별 품질 테스트만 추가하세요."
    elif quality >= 60:
        status = "tuning"
        recommendation = "노이즈 낮은 녹음 데이터를 30분 이상 추가 수집하세요."
    else:
        status = "collect_more_data"
        recommendation = "발음 교정 라벨과 감정 라벨을 보강한 데이터 재수집이 필요합니다."

    return {
        "profile_id": profile["profile_id"],
        "status": status,
        "quality_score": quality,
        "recommendation": recommendation,
    }


def synthesize_preview(profile: dict, text: str, style_strength: float) -> dict:
    style_words = ", ".join(profile.get("style_tags") or ["neutral"])
    speaking_rate = float(profile.get("speaking_rate", 1.0))
    pitch = float(profile.get("pitch_shift", 0.0))
    intensity = round(0.6 + style_strength * 0.8, 2)

    ssml = (
        f"<speak><prosody rate='{speaking_rate:.2f}' pitch='{pitch:+.1f}st'>"
        f"<emphasis level='moderate'>{text}</emphasis>"
        "</prosody></speak>"
    )

    preview = (
        f"[{profile['name']}]({profile.get('base_voice','default')}) "
        f"스타일={style_words}, 감정강도={intensity}로 낭독: {text}"
    )

    return {
        "profile_id": profile["profile_id"],
        "provider": "local-preview",
        "preview_text": preview,
        "ssml_preview": ssml,
    }
