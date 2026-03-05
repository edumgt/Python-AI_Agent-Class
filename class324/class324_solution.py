"""
class324 advanced practice script
교과구분: 정규교과-6
교과목명: 거대 언어 모델을 활용한 자연어 생성
차시 주제: 대화형 응답 설계
교육일차: Day 41
일일 교시: 4교시 (1일 8시간 운영 기준)
난이도: 기초응용
실행 방법:
    python class324.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS324"
SUBJECT = "거대 언어 모델을 활용한 자연어 생성"
MODULE = "대화형 응답 설계"
DAY = "Day 41"
SLOT = "4교시"
SESSION = 36


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


def build_prompt(user_input: str) -> str:
    system = "당신은 친절한 AI 튜터입니다."
    return f"[SYSTEM] {system}\n[USER] {user_input}\n[ASSISTANT]"


def run_practice():
    user_input = f"{MODULE} 주제를 3문장으로 설명해줘."
    prompt = build_prompt(user_input)
    mock_response = {
        "model": "demo-llm",
        "tokens_estimate": len(prompt.split()),
        "response_preview": shorten(f"{MODULE} 학습을 위한 예시 응답입니다. 핵심 개념, 절차, 주의점을 포함합니다.", width=60),
    }

    lines = [
        "LLM 입력/출력 구조 실습",
        f"- 생성 프롬프트:\n{prompt}",
        f"- 모의 응답 메타데이터: {mock_response}",
    ]

    if "API" in MODULE or "모델" in MODULE:
        request_example = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful tutor."},
                {"role": "user", "content": user_input},
            ],
        }
        lines.append(f"- API 요청 예시: {request_example}")

    text = "\n\n".join(lines)
    print(text)
    out_file = save_output("class324_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
