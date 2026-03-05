"""
class499 assignment
교과목명: RAG(Retrieval-Augmented Generation)
차시 주제: 실전 RAG 미니 프로젝트
교육일차: Day 63
일일 교시: 3교시 (1일 8시간 운영 기준)

진행(권장):
- 설명 10분: 문제/목표 공유, 예제 시연
- 실습 30분: TODO 구현
- 정리 10분: 리뷰 + 개선 포인트

차시 목표(요약):
- 실전 RAG 미니 프로젝트 핵심 개념 이해
- 실전 RAG 미니 프로젝트 관련 코드/도구 적용
- 실전 RAG 미니 프로젝트 결과 점검 및 다음 차시 연결
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
