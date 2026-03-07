# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class109 advanced practice script
교과구분: 정규교과-3
교과목명: 머신러닝과 딥러닝
차시 주제: 특성공학과 전처리
교육일차: Day 14
일일 교시: 5교시 (1일 8시간 운영 기준)
난이도: 기초응용
실행 방법:
    python class109.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS109"
SUBJECT = "머신러닝과 딥러닝"
MODULE = "특성공학과 전처리"
DAY = "Day 14"
SLOT = "5교시"
SESSION = 29


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
    x = [1, 2, 3, 4, 5]
    y = [2 * v + 3 for v in x]

    try:
        from sklearn.linear_model import LinearRegression
        import numpy as np
        model = LinearRegression()
        model.fit(np.array(x).reshape(-1, 1), np.array(y))
        prediction = float(model.predict([[6]])[0])
        text = (
            "scikit-learn 회귀 실습\n"
            f"coef={model.coef_[0]:.2f}, intercept={model.intercept_:.2f}\n"
            f"x=6 예측값={prediction:.2f}"
        )
    except Exception:
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        nume = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
        deno = sum((a - mean_x) ** 2 for a in x)
        slope = nume / deno
        intercept = mean_y - slope * mean_x
        prediction = slope * 6 + intercept
        text = (
            "기초 선형회귀 수식 실습\n"
            f"slope={slope:.2f}, intercept={intercept:.2f}\n"
            f"x=6 예측값={prediction:.2f}"
        )

    if "딥러닝" in MODULE:
        hidden = [max(0, 0.8 * v - 1) for v in x]
        text += "\n\n간단한 ReLU 은닉층 출력: " + str(hidden)

    print(text)
    out_file = save_output("class109_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
