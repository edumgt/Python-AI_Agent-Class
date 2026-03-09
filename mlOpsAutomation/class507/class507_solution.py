# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class507 advanced practice script
교과구분: 프로젝트-1
교과목명: 프로젝트
차시 주제: MLOps 파이프라인과 모델 레지스트리 · 단계 2/5 기초 구현 [class507]
교육일차: Day 64
일일 교시: 3교시 (1일 8시간 운영 기준)
난이도: 기초응용
실행 방법:
    python class507.py
"""

from __future__ import annotations

from pathlib import Path


CLASS_ID = "CLASS507"
SUBJECT = "프로젝트"
MODULE = "MLOps 파이프라인과 모델 레지스트리 · 단계 2/5 기초 구현 [class507]"
DAY = "Day 64"
SLOT = "3교시"
SESSION = "7/20"


def print_header() -> None:
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


def run_practice() -> None:
    steps = [
        "요구사항 요약",
        "핵심 함수 구현",
        "예외/검증 추가",
        "운영 로그 점검",
    ]
    lines = [f"{idx}) {step}" for idx, step in enumerate(steps, start=1)]
    lines.append("- 결과: 모듈 주제 기반 실습 완료")
    text = "\n".join(lines)
    print(text)
    out_file = save_output("class507_result.txt", text)
    print(f"\n산출물 저장: {out_file}")


def main() -> None:
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
