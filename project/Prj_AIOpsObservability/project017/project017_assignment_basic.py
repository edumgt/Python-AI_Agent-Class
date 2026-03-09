# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
project017 Basic(입문) 과제 (자기주도 학습용)

[학습 정보]
- 교과목: 프로젝트
- 주제: AIOps 관측성·이상탐지·자동복구 · 단계 2/5 기초 구현 [project017]
- 일정: Day 65 / 5교시
- 난이도: 기초응용

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
- python project/Prj_AIOpsObservability/project017/project017_assignment_basic.py

[쉬운 학습 포인트]
- 표 데이터를 정리해서 의미를 찾는 연습을 해요.
- 열 이름을 먼저 확인하고, 어떤 숫자를 계산할지 순서를 정하세요.

[진행 순서]
1) TODO 지시문을 먼저 읽고, 입력/출력 예시를 적어 봅니다.
2) TODO를 1개 구현한 뒤 바로 실행해 확인합니다.
3) 오류가 나면 에러 마지막 줄을 보고 수정합니다.
4) 모든 TODO 완료 후 한 번 더 전체 실행합니다.

[디버깅 힌트]
- shape/columns를 출력하면 데이터 구조 오류를 빠르게 찾을 수 있어요.
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
