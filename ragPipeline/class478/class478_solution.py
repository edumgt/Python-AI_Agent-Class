# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class478 advanced practice script
교과구분: 정규교과-9
교과목명: RAG(Retrieval-Augmented Generation)
차시 주제: 검색 품질 개선
교육일차: Day 60
일일 교시: 6교시 (1일 8시간 운영 기준)
난이도: 기초응용
실행 방법:
    python class478.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS478"
SUBJECT = "RAG(Retrieval-Augmented Generation)"
MODULE = "검색 품질 개선"
DAY = "Day 60"
SLOT = "6교시"
SESSION = 30


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


def chunk_text(text: str, size: int = 30) -> list[str]:
    return [text[i:i+size] for i in range(0, len(text), size)]


def retrieve(query: str, chunks: list[str]) -> list[str]:
    scored = []
    q_tokens = set(query.split())
    for chunk in chunks:
        c_tokens = set(chunk.split())
        score = len(q_tokens & c_tokens)
        scored.append((score, chunk))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [chunk for score, chunk in scored[:2] if score >= 0]


def run_practice():
    document = (
        "RAG는 문서를 분할하고, 질문과 관련된 청크를 검색한 뒤, "
        "검색된 내용을 바탕으로 응답을 생성하는 구조입니다. "
        "벡터DB, 임베딩, 리랭킹, 프롬프트 결합이 핵심입니다."
    )
    chunks = chunk_text(document)
    query = "RAG 임베딩 프롬프트"
    top_chunks = retrieve(query, chunks)

    text = (
        "RAG 미니 파이프라인 실습\n"
        f"- 문서 청크 수: {len(chunks)}\n"
        f"- 질의: {query}\n"
        f"- 검색 결과: {top_chunks}"
    )
    print(text)
    out_file = save_output("class478_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
