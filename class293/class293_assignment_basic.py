"""
class293 assignment
교과목명: 거대 언어 모델을 활용한 자연어 생성
차시 주제: LLM 개요
교육일차: Day 37
일일 교시: 5교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- LLM 개요 핵심 개념 이해
- LLM 개요 관련 코드/도구 적용
- LLM 개요 결과 점검 및 다음 차시 연결
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
