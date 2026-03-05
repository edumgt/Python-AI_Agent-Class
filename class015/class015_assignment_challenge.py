"""
class015 assignment
교과목명: Python 프로그래밍
차시 주제: 반복문과 흐름제어
교육일차: Day 02
일일 교시: 7교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- 반복문과 흐름제어 핵심 개념 이해
- 반복문과 흐름제어 관련 코드/도구 적용
- 반복문과 흐름제어 결과 점검 및 다음 차시 연결
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
        "class_id": "class015",
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
