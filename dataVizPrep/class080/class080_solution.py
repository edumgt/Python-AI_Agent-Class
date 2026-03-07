# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class080 advanced practice script
교과구분: 정규교과-2
교과목명: Python 전처리 및 시각화
차시 주제: 전처리+시각화 미니 프로젝트
교육일차: Day 10
일일 교시: 8교시 (1일 8시간 운영 기준)
난이도: 실전심화
실행 방법:
    python class080.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS080"
SUBJECT = "Python 전처리 및 시각화"
MODULE = "전처리+시각화 미니 프로젝트"
DAY = "Day 10"
SLOT = "8교시"
SESSION = 40


def print_header():
    print("=" * 72)
    print(f"{CLASS_ID} | {SUBJECT}")
    print(f"주제: {MODULE}")
    print(f"일정: {DAY} / {SLOT}")
    print(f"세부 시퀀스: {SESSION}")
    print("=" * 72)


def save_output(name: str, text: str) -> Path:
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / name
    out_file.write_text(text, encoding="utf-8")
    return out_file


def run_practice():
    rows = [
        {"name": "A", "score": 70 + SESSION, "hours": 2 + (SESSION % 3)},
        {"name": "B", "score": 65 + SESSION, "hours": 3 + (SESSION % 2)},
        {"name": "C", "score": 80 + SESSION, "hours": 1 + (SESSION % 4)},
    ]

    try:
        import pandas as pd
        df = pd.DataFrame(rows)
        df["efficiency"] = (df["score"] / df["hours"]).round(2)
        summary = df.describe(include="all").fillna("")
        text = "데이터프레임\n" + df.to_string(index=False) + "\n\n요약\n" + summary.to_string()
        print(text)

        if "시각화" in MODULE:
            try:
                import matplotlib.pyplot as plt
                plt.figure(figsize=(6, 4))
                plt.plot(df["name"], df["score"], marker="o")
                plt.title(f"{CLASS_ID} Score Trend")
                plt.xlabel("name")
                plt.ylabel("score")
                img_path = Path(__file__).resolve().parent / "outputs"
                img_path.mkdir(exist_ok=True)
                chart = img_path / "class080_chart.png"
                plt.tight_layout()
                plt.savefig(chart)
                plt.close()
                print(f"\n차트 저장: {chart}")
            except Exception as e:
                print(f"\n차트 생성 생략: {e}")
    except Exception:
        scores = [row["score"] for row in rows]
        avg = round(sum(scores) / len(scores), 2)
        text = f"pandas 미설치 환경\nrows={rows}\n평균 score={avg}"
        print(text)

    out_file = save_output("class080_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
