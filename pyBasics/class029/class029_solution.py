# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class029 advanced practice script
교과구분: 정규교과-1
교과목명: Python 프로그래밍
차시 주제: 예외처리와 디버깅
교육일차: Day 04
일일 교시: 5교시 (1일 8시간 운영 기준)
난이도: 실전심화
실행 방법:
    python class029.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS029"
SUBJECT = "Python 프로그래밍"
MODULE = "예외처리와 디버깅"
DAY = "Day 04"
SLOT = "5교시"
SESSION = 29


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


def run_practice():
    sample_numbers = [29, 30, 31, 32]
    squares = [n * n for n in sample_numbers]
    even_numbers = [n for n in sample_numbers if n % 2 == 0]

    result = []
    result.append("1) 기본 리스트 생성")
    result.append(f"   - 원본: {sample_numbers}")
    result.append("2) 리스트 컴프리헨션")
    result.append(f"   - 제곱값: {squares}")
    result.append("3) 조건 필터링")
    result.append(f"   - 짝수: {even_numbers}")

    if "함수" in MODULE:
        def multiply(a: int, b: int) -> int:
            return a * b
        result.append("4) 함수 실습")
        result.append(f"   - multiply(3, 4) = {multiply(3, 4)}")

    if "객체" in MODULE:
        class Learner:
            def __init__(self, name: str, progress: int) -> None:
                self.name = name
                self.progress = progress
            def summary(self) -> str:
                return f"{self.name} / 진도 {self.progress}%"
        learner = Learner("student", 10 + SESSION)
        result.append("4) 객체 생성")
        result.append(f"   - {learner.summary()}")

    text = "\n".join(result)
    print(text)
    out_file = save_output("class029_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
