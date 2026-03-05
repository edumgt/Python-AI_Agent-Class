"""
class094 assignment
교과목명: 머신러닝과 딥러닝
차시 주제: 회귀 모델
교육일차: Day 12
일일 교시: 6교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- 회귀 모델 핵심 개념 이해
- 회귀 모델 관련 코드/도구 적용
- 회귀 모델 결과 점검 및 다음 차시 연결
"""
from __future__ import annotations

from pathlib import Path
import math
import statistics
import json
import random


import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# =========================
# TODO 1) 데이터 생성
# - y = 3x + noise 형태의 샘플을 생성하라.
# =========================
def make_data(n: int = 50, seed: int = 42):
    # TODO: X(2D), y(1D)
    raise NotImplementedError

# =========================
# TODO 2) 모델 학습 & 평가
# - LinearRegression 학습 후 MSE를 출력하라.
# =========================
def train_and_eval(X, y) -> float:
    # TODO
    raise NotImplementedError

def main():
    X, y = make_data()
    mse = train_and_eval(X, y)
    print("MSE:", mse)

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
        "class_id": "class094",
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
