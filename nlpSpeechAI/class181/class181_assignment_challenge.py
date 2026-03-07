# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class181 Challenge(챌린지) 과제 (자기주도 학습용)

[학습 정보]
- 교과목: 자연어 및 음성 데이터 활용 및 모델 개발
- 주제: 오디오 전처리
- 일정: Day 23 / 5교시
- 난이도: 기초응용

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
- python nlpSpeechAI/class181/class181_assignment_challenge.py

[쉬운 학습 포인트]
- 음성 데이터를 규칙적으로 다루는 연습을 해요.
- 파일/길이/라벨 같은 필수 항목이 있는지 먼저 확인하세요.

[진행 순서]
1) TODO 지시문을 먼저 읽고, 입력/출력 예시를 적어 봅니다.
2) TODO를 1개 구현한 뒤 바로 실행해 확인합니다.
3) 오류가 나면 에러 마지막 줄을 보고 수정합니다.
4) 모든 TODO 완료 후 한 번 더 전체 실행합니다.

[디버깅 힌트]
- 샘플 3개만 먼저 출력해서 형식이 맞는지 검증하세요.
- 함수 분리 -> assert 테스트 -> 성능 로그 순서로 진행하세요.
"""


from __future__ import annotations

from pathlib import Path
import math
import statistics
import json
import random


import pandas as pd

# =========================
# TODO 1) DataFrame 만들기
# - 아래 rows로 DataFrame을 생성하고, 총합/평균 컬럼을 추가하라.
# =========================
rows = [
    {"name": "A", "score1": 80, "score2": 90},
    {"name": "B", "score1": 75, "score2": 60},
    {"name": "C", "score1": 92, "score2": 88},
]

def build_df(rows: list[dict]) -> pd.DataFrame:
    # TODO
    raise NotImplementedError

# =========================
# TODO 2) CSV 저장 & 다시 읽기
# - outputs/data.csv로 저장 후 다시 읽어서 shape를 출력하라.
# =========================
def save_and_load(df: pd.DataFrame) -> pd.DataFrame:
    # TODO
    raise NotImplementedError

def main():
    df = build_df(rows)
    print(df)
    df2 = save_and_load(df)
    print("loaded shape:", df2.shape)

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
        "class_id": "class181",
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
