# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class028 example1: 파일 입출력 · 단계 4/4 운영 최적화 [class028]"""

TOPIC = "파일 입출력 · 단계 4/4 운영 최적화 [class028]"
EXAMPLE_TEMPLATE = "file_io"

import json
from pathlib import Path

def write_rows(rows):
    out = Path(__file__).with_name("class028_logs.jsonl")
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

if __name__ == "__main__":
    main()
