"""
class447 assignment
교과목명: Langchain 활용하기
차시 주제: 실전 체인 애플리케이션
교육일차: Day 56
일일 교시: 7교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- 실전 체인 애플리케이션 핵심 개념 이해
- 실전 체인 애플리케이션 관련 코드/도구 적용
- 실전 체인 애플리케이션 결과 점검 및 다음 차시 연결
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
# ADVANCED 확장 과제
# =========================
def advanced_extension():
    """심화 과제: 기본 과제를 '조금 더 실무형'으로 확장합니다.

    TODO(심화):
    1) 입력값 검증을 강화하고, 실패 케이스를 예외로 처리하세요.
    2) 결과를 dict로 정리해 JSON 파일로 저장하세요. (파일명: class447_advanced_result.json)
    3) 표준 라이브러리만 사용해서 간단한 리포트(텍스트)를 출력하세요.
    """
    # TODO: 아래는 예시 스켈레톤입니다. 필요한 로직을 채우세요.
    result = {
        "class_id": "class447",
        "tier": "advanced",
        "summary": "TODO: 실습 결과 요약",
    }
    # TODO: JSON 저장
    # from pathlib import Path
    # import json
    # Path(__file__).with_name("class447_advanced_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    # 기존 main 흐름을 유지하고, 마지막에 심화 확장 실행
    try:
        # 파일 내에 main()이 있다면 호출
        main  # type: ignore[name-defined]
    except Exception:
        pass
    else:
        try:
            main()  # type: ignore[misc]
        except TypeError:
            # main이 인자를 요구하면 스킵
            pass

    print("\n[ADVANCED] extension running...")
    out = advanced_extension()
    print(out)
