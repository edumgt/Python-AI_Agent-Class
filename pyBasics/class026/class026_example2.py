# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class026 example2: 파일 입출력 · 단계 2/4 기초 구현 [class026]"""

TOPIC = "파일 입출력 · 단계 2/4 기초 구현 [class026]"
EXAMPLE_TEMPLATE = "file_io"

import json
from pathlib import Path

def write_rows(rows):
    out = Path(__file__).with_name("class026_logs.jsonl")
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
