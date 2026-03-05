"""
class448 advanced practice script
교과구분: 정규교과-8
교과목명: Langchain 활용하기
차시 주제: 실전 체인 애플리케이션
교육일차: Day 56
일일 교시: 8교시 (1일 8시간 운영 기준)
난이도: 실전심화
실행 방법:
    python class448.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS448"
SUBJECT = "Langchain 활용하기"
MODULE = "실전 체인 애플리케이션"
DAY = "Day 56"
SLOT = "8교시"
SESSION = 56


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
    out_file = save_output("class448_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
