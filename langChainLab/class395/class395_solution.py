# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class395 advanced practice script
교과구분: 정규교과-8
교과목명: Langchain 활용하기
차시 주제: LangChain 개요
교육일차: Day 50
일일 교시: 3교시 (1일 8시간 운영 기준)
난이도: 입문
실행 방법:
    python class395.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS395"
SUBJECT = "Langchain 활용하기"
MODULE = "LangChain 개요"
DAY = "Day 50"
SLOT = "3교시"
SESSION = 3


def print_header():
    print("=" * 72)
    print(f"{CLASS_ID} | {SUBJECT}")
    print(f"주제: {MODULE}")
    print(f"일정: {DAY} / {SLOT}")
    print(f"세부 시퀀스: {SESSION}")
    print("=" * 72)


def save_output(name: str, text: str) -> Path:
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / name
    out_file.write_text(text, encoding="utf-8")
    return out_file


class SimpleChain:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def invoke(self, question: str) -> str:
        return f"{self.prefix} | 질문: {question} | 요약 응답 생성"


def run_practice():
    question = f"{MODULE} 핵심 흐름을 설명해줘."
    chain = SimpleChain("LangChain-like Demo")
    demo_result = chain.invoke(question)

    lines = [
        "체인 구성 실습",
        f"- 입력 질문: {question}",
        f"- 체인 응답: {demo_result}",
    ]

    try:
        from langchain_core.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_template("질문: {question}")
        lines.append(f"- 실제 LangChain PromptTemplate 사용 가능: {prompt is not None}")
    except Exception:
        lines.append("- 실제 LangChain 미설치 시에도 현재 데모 체인으로 흐름 이해 가능")

    text = "\n".join(lines)
    print(text)
    out_file = save_output("class395_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
