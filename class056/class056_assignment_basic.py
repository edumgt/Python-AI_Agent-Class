"""
class056 assignment
교과목명: Python 전처리 및 시각화
차시 주제: 결측치/이상치 처리
교육일차: Day 07
일일 교시: 8교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- 결측치/이상치 처리 핵심 개념 이해
- 결측치/이상치 처리 관련 코드/도구 적용
- 결측치/이상치 처리 결과 점검 및 다음 차시 연결
"""
from __future__ import annotations

from pathlib import Path
import math
import statistics
import json
import random


import pandas as pd
import matplotlib.pyplot as plt

# =========================
# TODO 1) 간단 데이터 준비
# =========================
x = list(range(1, 11))
y = [v * v for v in x]

# =========================
# TODO 2) 라인 차트 그리기
# - 제목/축라벨 포함
# - outputs/plot.png 로 저장
# =========================
def make_plot(x: list[int], y: list[int]) -> Path:
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "plot.png"
    # TODO: plot + savefig
    raise NotImplementedError

def main():
    out = make_plot(x, y)
    print("saved:", out)

if __name__ == "__main__":
    main()
