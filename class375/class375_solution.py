"""
class375 advanced practice script
교과구분: 정규교과-7
교과목명: 프롬프트 엔지니어링
차시 주제: 단계적 추론 유도
교육일차: Day 47
일일 교시: 7교시 (1일 8시간 운영 기준)
난이도: 기초응용
실행 방법:
    python class375.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS375"
SUBJECT = "프롬프트 엔지니어링"
MODULE = "단계적 추론 유도"
DAY = "Day 47"
SLOT = "7교시"
SESSION = 23


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


def score_prompt(prompt: str) -> dict[str, int]:
    return {
        "clarity": 20 if "목표" in prompt else 10,
        "context": 20 if "배경" in prompt else 10,
        "format": 20 if "형식" in prompt else 10,
        "constraints": 20 if "제약" in prompt else 10,
        "examples": 20 if "예시" in prompt else 10,
    }


def run_practice():
    prompt = (
        "목표: 단계적 추론 유도 실습 가이드를 작성하라\n"
        "배경: AI 교육 과정 초급 학습자\n"
        "형식: 체크리스트\n"
        "제약: 5단계 이내\n"
        "예시: 간단한 샘플 포함"
    )
    scores = score_prompt(prompt)
    total = sum(scores.values())

    text = (
        "프롬프트 품질 점검 실습\n"
        f"프롬프트 초안:\n{prompt}\n\n"
        f"평가 항목: {scores}\n"
        f"총점: {total} / 100"
    )
    print(text)
    out_file = save_output("class375_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
