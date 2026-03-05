"""
class020 assignment
교과목명: Python 프로그래밍
차시 주제: 함수와 모듈
교육일차: Day 03
일일 교시: 4교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- 함수와 모듈 핵심 개념 이해
- 함수와 모듈 관련 코드/도구 적용
- 함수와 모듈 결과 점검 및 다음 차시 연결
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
