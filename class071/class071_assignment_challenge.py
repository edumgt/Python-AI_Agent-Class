"""
class071 assignment
교과목명: Python 전처리 및 시각화
차시 주제: Matplotlib 시각화 기초
교육일차: Day 09
일일 교시: 7교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- Matplotlib 시각화 기초 핵심 개념 이해
- Matplotlib 시각화 기초 관련 코드/도구 적용
- Matplotlib 시각화 기초 결과 점검 및 다음 차시 연결
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


# =========================
# CHALLENGE 확장 과제
# =========================
def challenge_extension():
    """챌린지 과제: 테스트/성능/구조화 관점까지 다룹니다.

    TODO(챌린지):
    1) 입력/출력 로직을 함수로 분리해 재사용 가능하게 리팩토링하세요.
    2) '자체 테스트'를 최소 3개 이상 작성하세요. (assert 기반)
    3) 실행 시간을 측정하고(예: time.perf_counter), 간단한 성능 로그를 남기세요.
    """
    import time
    t0 = time.perf_counter()

    # TODO: 리팩토링 된 함수를 호출해서 결과를 생성하세요.
    result = {
        "class_id": "class071",
        "tier": "challenge",
        "checks": ["TODO: assert 1", "TODO: assert 2", "TODO: assert 3"],
    }

    t1 = time.perf_counter()
    result["elapsed_ms"] = round((t1 - t0) * 1000, 3)
    return result


if __name__ == "__main__":
    try:
        main  # type: ignore[name-defined]
    except Exception:
        pass
    else:
        try:
            main()  # type: ignore[misc]
        except TypeError:
            pass

    print("\n[CHALLENGE] extension running...")
    out = challenge_extension()
    print(out)
