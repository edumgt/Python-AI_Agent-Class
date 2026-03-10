# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class025 example4: 파일 입출력 · 단계 1/4 입문 이해 [class025]"""

TOPIC = "파일 입출력 · 단계 1/4 입문 이해 [class025]"
EXAMPLE_TEMPLATE = "file_io"
EXAMPLE_VARIANT = 4

import csv
from pathlib import Path

def write_text_summary(rows, out_path):
    lines = [f"{row['name']},{row['score']}" for row in rows]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path

def write_csv_rows(rows, out_path):
    with out_path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=["name", "score"])
        writer.writeheader()
        writer.writerows(rows)
    return out_path

def read_csv_rows(path):
    with path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        return [{"name": row["name"], "score": int(row["score"])} for row in reader]

def build_rows():
    rows = [
        {"name": "A", "score": 72},
        {"name": "B", "score": 88},
        {"name": "C", "score": 91},
    ]
    if EXAMPLE_VARIANT >= 2:
        rows.append({"name": "D", "score": 67})
    if EXAMPLE_VARIANT >= 3:
        rows.append({"name": "E", "score": 95})
    if EXAMPLE_VARIANT >= 4:
        rows.append({"name": "F", "score": 84})
    if EXAMPLE_VARIANT >= 5:
        rows.append({"name": "G", "score": 78})
    return rows

def run_automation(base_dir):
    text_path = base_dir / "class025_summary.txt"
    csv_path = base_dir / "class025_scores.csv"
    rows = build_rows()
    write_text_summary(rows, text_path)
    write_csv_rows(rows, csv_path)
    loaded = read_csv_rows(csv_path)
    passed = [row for row in loaded if row["score"] >= 80]
    return {
        "text_file": text_path.name,
        "csv_file": csv_path.name,
        "row_count": len(loaded),
        "pass_count": len(passed),
    }

def main():
    print("오늘 주제:", TOPIC)
    out_dir = Path(__file__).parent
    report = run_automation(out_dir)
    print("파일 리포트:", report)
    return {"variant": EXAMPLE_VARIANT, **report}

def mini_project_plan():
    return {
        "scenario": "입출력 자동화 파이프라인(읽기-가공-쓰기)을 완성하세요.",
        "steps": [
            "1) baseline 실행",
            "2) 개선안 적용",
            "3) 지표/로그 비교",
        ],
        "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("미니 프로젝트:", mini_project_plan())
