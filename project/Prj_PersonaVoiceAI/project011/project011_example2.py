# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""project011 example2: 사전 데이터 기반 PERSONA AI 구축 · 단계 1/5 입문 이해 [project011]"""

TOPIC = "사전 데이터 기반 PERSONA AI 구축 · 단계 1/5 입문 이해 [project011]"
EXAMPLE_TEMPLATE = "persona_project"
EXAMPLE_VARIANT = 2

import statistics

def _safe_mean(values):
    return float(statistics.fmean(values)) if values else 0.0

def _safe_std(values):
    return float(statistics.pstdev(values)) if len(values) >= 2 else 0.0

def detect_phase(topic):
    if "음성봇" in topic:
        return "foundation"
    if "stt" in topic.lower() and "tts" in topic.lower():
        return "pipeline"
    if "사전 데이터" in topic:
        return "dataset"
    return "continuous"

def build_payload(variant):
    base = [0.72, 0.68, 0.75]
    note = "baseline"
    if variant >= 2:
        base = [0.81, 0.63, 0.77, 0.69]
        note = "diverse-input"
    if variant >= 3:
        base = [0.52, 0.79, 0.41, 0.74]
        note = "failure-mixed"
    if variant >= 4:
        base = [0.84, 0.78, 0.82, 0.76, 0.79]
        note = "data-driven-tuning"
    if variant >= 5:
        base = [0.87, 0.75, 0.83, 0.79, 0.72, 0.81]
        note = "continual-learning"
    return {"values": base, "note": note}

def evaluate_persona(topic, values):
    phase = detect_phase(topic)
    avg = _safe_mean(values)
    std = _safe_std(values)

    if phase == "foundation":
        profile_score = round(avg * 100, 2)
        status = "ready" if profile_score >= 70 else "design"
        return {
            "phase": "개인 맞춤 코칭 음성봇 기초 구축",
            "status": status,
            "profile_score": profile_score,
            "rule_consistency": round((1.0 - std) * 100, 2),
        }
    if phase == "pipeline":
        loop_quality = round(max(0.0, min(1.0, avg - std * 0.4)) * 100, 2)
        status = "stable" if loop_quality >= 68 else "tune"
        return {
            "phase": "STT-LLM-TTS 코칭 대화 루프",
            "status": status,
            "loop_quality": loop_quality,
            "latency_hint_ms": int((0.18 + std) * 1000),
        }
    if phase == "dataset":
        dataset_quality = round((avg * 0.7 + (1.0 - std) * 0.3) * 100, 2)
        status = "usable" if dataset_quality >= 72 else "relabel"
        return {
            "phase": "사전 데이터 기반 PERSONA 구축",
            "status": status,
            "dataset_quality": dataset_quality,
            "label_consistency": round((1.0 - std) * 100, 2),
        }

    drift_score = round(((1.0 - avg) + std) * 100, 2)
    status = "retrain" if drift_score >= 35 else "monitor"
    return {
        "phase": "PERSONA 지속학습 운영",
        "status": status,
        "drift_score": drift_score,
        "next_action": "재학습 큐 등록" if status == "retrain" else "모니터링 유지",
    }

def main():
    print("오늘 주제:", TOPIC)
    payload = build_payload(EXAMPLE_VARIANT)
    result = evaluate_persona(TOPIC, payload["values"])
    result["variant"] = EXAMPLE_VARIANT
    result["note"] = payload["note"]
    print("샘플 입력:", payload["values"])
    print("평가 결과:", result)
    return result

def extension_mission():
    return {
        "mission": "입력값 2세트를 비교하고 차이를 기록하세요.",
        "check": "예외 케이스 1개를 추가해 방어 로직을 검증하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
