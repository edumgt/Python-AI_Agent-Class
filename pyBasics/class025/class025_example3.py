# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class025 example3: 파일 입출력 · 단계 1/4 입문 이해 [class025]"""

TOPIC = "파일 입출력 · 단계 1/4 입문 이해 [class025]"
EXAMPLE_TEMPLATE = "file_io"

import json
from pathlib import Path

def write_rows(rows):
    out = Path(__file__).with_name("class025_logs.jsonl")
    payload = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    out.write_text(payload + "\n", encoding="utf-8")
    return out

def read_rows(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def main():
    print("오늘 주제:", TOPIC)
    source = [
        {"step": "extract", "ok": True},
        {"step": "transform", "ok": True},
        {"step": "load", "ok": False},
    ]
    path = write_rows(source)
    loaded = read_rows(path)
    print("저장 파일:", path.name)
    print("복원 행 수:", len(loaded))
    return {"file": path.name, "loaded": len(loaded)}

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "핵심 함수를 재사용 가능한 모듈로 분리하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
