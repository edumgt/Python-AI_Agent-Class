# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class507 solution
교과구분: 정규교과-10
교과목명: LLMOps
차시 주제: 프롬프트 관리
교육일차: Day 64
일일 교시: 7교시
난이도: 실전심화
"""
from __future__ import annotations
from pathlib import Path

CLASS_ID = "CLASS507"
SUBJECT  = "LLMOps"
MODULE   = "프롬프트 관리"
DAY      = "Day 64"
SLOT     = "7교시"


def print_header():
    print("=" * 72)
    print(f"{CLASS_ID} | {SUBJECT}")
    print(f"주제: {MODULE}")
    print(f"일정: {DAY} / {SLOT}")
    print("=" * 72)


def save_output(name: str, text: str) -> Path:
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / name
    out_file.write_text(text, encoding="utf-8")
    return out_file


class LLMOpsDemo:
    def __init__(self, module: str) -> None:
        self.module = module

    def invoke(self, question: str) -> str:
        return f"{self.module} | 질문: {question} | LLMOps 시연 응답"


def run_practice():
    question = f"{MODULE} 핵심 흐름을 설명해줘."
    demo = LLMOpsDemo(MODULE)
    result = demo.invoke(question)
    lines = [
        f"[class507] 프롬프트 관리 단계 3/4 실전 검증",
        f"  입력: {question}",
        f"  출력: {result}",
        "  점검: 핵심 개념 이해 완료",
    ]
    report = "\n".join(lines)
    out_path = save_output("class507_result.txt", report)
    print(report)
    print(f"  저장: {out_path}")
    return report


if __name__ == "__main__":
    print_header()
    run_practice()
