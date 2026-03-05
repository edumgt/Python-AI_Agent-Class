"""
class084 assignment
교과목명: 머신러닝과 딥러닝
차시 주제: ML/DL 개요와 문제정의
교육일차: Day 11
일일 교시: 4교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- ML/DL 개요와 문제정의 핵심 개념 이해
- ML/DL 개요와 문제정의 관련 코드/도구 적용
- ML/DL 개요와 문제정의 결과 점검 및 다음 차시 연결
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
# ADVANCED 확장 과제
# =========================
def advanced_extension():
    """심화 과제: 기본 과제를 '조금 더 실무형'으로 확장합니다.

    TODO(심화):
    1) 입력값 검증을 강화하고, 실패 케이스를 예외로 처리하세요.
    2) 결과를 dict로 정리해 JSON 파일로 저장하세요. (파일명: class084_advanced_result.json)
    3) 표준 라이브러리만 사용해서 간단한 리포트(텍스트)를 출력하세요.
    """
    # TODO: 아래는 예시 스켈레톤입니다. 필요한 로직을 채우세요.
    result = {
        "class_id": "class084",
        "tier": "advanced",
        "summary": "TODO: 실습 결과 요약",
    }
    # TODO: JSON 저장
    # from pathlib import Path
    # import json
    # Path(__file__).with_name("class084_advanced_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
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
