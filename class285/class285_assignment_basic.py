"""
class285 assignment
교과목명: 음성 데이터 활용한 TTS와 STT 모델 개발
차시 주제: 실전 음성 모델 데모
교육일차: Day 36
일일 교시: 5교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- 실전 음성 모델 데모 핵심 개념 이해
- 실전 음성 모델 데모 관련 코드/도구 적용
- 실전 음성 모델 데모 결과 점검 및 다음 차시 연결
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
