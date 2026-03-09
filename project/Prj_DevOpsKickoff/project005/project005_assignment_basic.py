# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
project005 Basic(입문) 과제 (자기주도 학습용)

[학습 정보]
- 교과목: 프로젝트
- 주제: DevOps 프로젝트 착수와 요구사항 정의 · 단계 5/5 운영 최적화 [project005]
- 일정: Day 64 / 1교시
- 난이도: 실전심화

[이번 과제 목표]
- 핵심 TODO를 완성해서 코드가 끝까지 실행되게 만들기
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
- python project/Prj_DevOpsKickoff/project005/project005_assignment_basic.py

[쉬운 학습 포인트]
- 데이터에서 규칙을 찾는 모델 사고를 연습해요.
- 입력(X)과 정답(y)의 형태를 먼저 확인하고 학습 함수를 호출하세요.

[진행 순서]
1) TODO 지시문을 먼저 읽고, 입력/출력 예시를 적어 봅니다.
2) TODO를 1개 구현한 뒤 바로 실행해 확인합니다.
3) 오류가 나면 에러 마지막 줄을 보고 수정합니다.
4) 모든 TODO 완료 후 한 번 더 전체 실행합니다.

[디버깅 힌트]
- 오차(MSE/MAE)가 너무 크면 입력 스케일/분할 방식을 먼저 점검하세요.
- TODO 한 칸을 채울 때마다 바로 실행해서 확인하세요.
"""


from __future__ import annotations

from pathlib import Path
import math
import statistics
import json
import random


# 주의: 외부 LLM API 키 없이도 가능한 프롬프트/체인 설계 실습만 진행합니다.
from langchain_core.prompts import PromptTemplate

# =========================
# TODO 1) PromptTemplate 만들기
# - 변수: role, question
# =========================
def build_prompt() -> PromptTemplate:
    # TODO
    raise NotImplementedError

# =========================
# TODO 2) format 해서 출력
# =========================
def main():
    prompt = build_prompt()
    rendered = prompt.format(role="친절한 튜터", question="RAG가 뭐야?")
    print(rendered)

if __name__ == "__main__":
    main()
