"""
class077 assignment
교과목명: Python 전처리 및 시각화
차시 주제: 전처리+시각화 미니 프로젝트
교육일차: Day 10
일일 교시: 5교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- 전처리+시각화 미니 프로젝트 핵심 개념 이해
- 전처리+시각화 미니 프로젝트 관련 코드/도구 적용
- 전처리+시각화 미니 프로젝트 결과 점검 및 다음 차시 연결
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
# ADVANCED 확장 과제
# =========================
def advanced_extension():
    """심화 과제: 기본 과제를 '조금 더 실무형'으로 확장합니다.

    TODO(심화):
    1) 입력값 검증을 강화하고, 실패 케이스를 예외로 처리하세요.
    2) 결과를 dict로 정리해 JSON 파일로 저장하세요. (파일명: class077_advanced_result.json)
    3) 표준 라이브러리만 사용해서 간단한 리포트(텍스트)를 출력하세요.
    """
    # TODO: 아래는 예시 스켈레톤입니다. 필요한 로직을 채우세요.
    result = {
        "class_id": "class077",
        "tier": "advanced",
        "summary": "TODO: 실습 결과 요약",
    }
    # TODO: JSON 저장
    # from pathlib import Path
    # import json
    # Path(__file__).with_name("class077_advanced_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
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
