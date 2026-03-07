# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class298 Challenge(챌린지) 과제 (자기주도 학습용)

[학습 정보]
- 교과목: 거대 언어 모델을 활용한 자연어 생성
- 주제: 토큰/컨텍스트 이해
- 일정: Day 38 / 2교시
- 난이도: 입문

[이번 과제 목표]
- 리팩토링, 자체 테스트, 성능 확인까지 포함한 완성형으로 발전시키기
- 초등학생도 혼자 따라갈 수 있도록, 작은 단계로 나눠서 완성하기

[환경 구성 - Windows PowerShell]
1) cd C:\DevOps\Python-AI_Agent-Class
2) python -m venv .venv
3) .\.venv\Scripts\Activate.ps1
4) python -m pip install --upgrade pip
5) pip install -r requirements.txt

[환경 구성 - Linux/macOS (bash)]
1) cd /path/to/Python-AI_Agent-Class
2) python3 -m venv .venv
3) source .venv/bin/activate
4) python -m pip install --upgrade pip
5) pip install -r requirements.txt

[실행 방법]
- python class298/class298_assignment_challenge.py

[쉬운 학습 포인트]
- 문장을 토큰으로 나누고 패턴을 찾는 연습을 해요.
- 정제 -> 토큰화 -> 집계 순서를 고정하면 코드가 깔끔해져요.

[진행 순서]
1) TODO 지시문을 먼저 읽고, 입력/출력 예시를 적어 봅니다.
2) TODO를 1개 구현한 뒤 바로 실행해 확인합니다.
3) 오류가 나면 에러 마지막 줄을 보고 수정합니다.
4) 모든 TODO 완료 후 한 번 더 전체 실행합니다.

[디버깅 힌트]
- 토큰 리스트를 먼저 출력해 전처리 결과를 눈으로 확인하세요.
- 함수 분리 -> assert 테스트 -> 성능 로그 순서로 진행하세요.
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
        "class_id": "class298",
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
