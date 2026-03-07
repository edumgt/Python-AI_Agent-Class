# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class022 Challenge(챌린지) 과제 (자기주도 학습용)

[학습 정보]
- 교과목: Python 프로그래밍
- 주제: 컬렉션 자료구조
- 일정: Day 03 / 6교시
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
- python pyBasics/class022/class022_assignment_challenge.py

[쉬운 학습 포인트]
- 작은 규칙을 코드로 바꾸는 연습을 해요.
- 입력 -> 처리 -> 출력 흐름을 먼저 종이에 써 보고 코드를 작성하세요.

[진행 순서]
1) TODO 지시문을 먼저 읽고, 입력/출력 예시를 적어 봅니다.
2) TODO를 1개 구현한 뒤 바로 실행해 확인합니다.
3) 오류가 나면 에러 마지막 줄을 보고 수정합니다.
4) 모든 TODO 완료 후 한 번 더 전체 실행합니다.

[디버깅 힌트]
- print()로 중간 값을 찍어 보면 대부분의 실수를 바로 찾을 수 있어요.
- 함수 분리 -> assert 테스트 -> 성능 로그 순서로 진행하세요.
"""


from __future__ import annotations

from pathlib import Path
import math
import statistics
import json
import random


# =========================
# TODO 1) 입력/출력 & 자료구조
# - 아래 sample 리스트에서 짝수만 뽑아 제곱한 리스트를 만들어라.
# - 결과를 print 하라.
# =========================
sample = [1, 2, 3, 4, 5, 6]

def even_squares(nums: list[int]) -> list[int]:
    # TODO: 리스트 컴프리헨션으로 구현
    raise NotImplementedError

# =========================
# TODO 2) 함수 & 예외처리
# - divide(a,b)를 구현하되 b=0이면 ValueError를 발생시켜라.
# =========================
def divide(a: float, b: float) -> float:
    # TODO
    raise NotImplementedError

# =========================
# TODO 3) 파일 저장(실무형)
# - outputs/result.json 파일에 실습 결과를 저장하라.
# =========================
def save_result(payload: dict) -> Path:
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "result.json"
    # TODO: json 저장 (utf-8, indent=2)
    raise NotImplementedError

def main():
    print("== 실습 실행 ==")
    es = even_squares(sample)
    print("even_squares:", es)

    try:
        print("divide(10,2) =", divide(10, 2))
        print("divide(10,0) =", divide(10, 0))
    except Exception as e:
        print("예외 확인:", repr(e))

    payload = {"even_squares": es, "mean": statistics.mean(sample)}
    out = save_result(payload)
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
        "class_id": "class022",
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
