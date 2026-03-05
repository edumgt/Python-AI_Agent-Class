"""
class165 assignment
교과목명: 자연어 및 음성 데이터 활용 및 모델 개발
차시 주제: 언어모델 입력 구조
교육일차: Day 21
일일 교시: 5교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- 언어모델 입력 구조 핵심 개념 이해
- 언어모델 입력 구조 관련 코드/도구 적용
- 언어모델 입력 구조 결과 점검 및 다음 차시 연결
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
# ADVANCED 확장 과제
# =========================
def advanced_extension():
    """심화 과제: 기본 과제를 '조금 더 실무형'으로 확장합니다.

    TODO(심화):
    1) 입력값 검증을 강화하고, 실패 케이스를 예외로 처리하세요.
    2) 결과를 dict로 정리해 JSON 파일로 저장하세요. (파일명: class165_advanced_result.json)
    3) 표준 라이브러리만 사용해서 간단한 리포트(텍스트)를 출력하세요.
    """
    # TODO: 아래는 예시 스켈레톤입니다. 필요한 로직을 채우세요.
    result = {
        "class_id": "class165",
        "tier": "advanced",
        "summary": "TODO: 실습 결과 요약",
    }
    # TODO: JSON 저장
    # from pathlib import Path
    # import json
    # Path(__file__).with_name("class165_advanced_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
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
