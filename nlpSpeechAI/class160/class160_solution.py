# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class160 advanced practice script
교과구분: 정규교과-4
교과목명: 자연어 및 음성 데이터 활용 및 모델 개발
차시 주제: 임베딩 기초
교육일차: Day 20
일일 교시: 8교시 (1일 8시간 운영 기준)
난이도: 기초응용
실행 방법:
    python class160.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS160"
SUBJECT = "자연어 및 음성 데이터 활용 및 모델 개발"
MODULE = "임베딩 기초"
DAY = "Day 20"
SLOT = "8교시"
SESSION = 32


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


def tokenize(text: str) -> list[str]:
    cleaned = "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in text)
    return [tok for tok in cleaned.split() if tok]


def run_practice():
    sentence = "멀티모달 AI 시스템은 텍스트와 음성을 함께 다룹니다."
    tokens = tokenize(sentence)
    lengths = [len(t) for t in tokens]
    vocab = sorted(set(tokens))

    lines = []
    lines.append("텍스트 전처리 실습")
    lines.append(f"- 원문: {sentence}")
    lines.append(f"- 토큰: {tokens}")
    lines.append(f"- 고유어휘: {vocab}")
    lines.append(f"- 평균 토큰 길이: {statistics.mean(lengths):.2f}")

    if "음성" in MODULE:
        import wave
        out_dir = Path(__file__).resolve().parent / "outputs"
        out_dir.mkdir(exist_ok=True)
        wav_path = out_dir / "class160_beep.wav"
        sample_rate = 8000
        duration = 0.2
        frames = bytearray()
        for i in range(int(sample_rate * duration)):
            value = int(10000 * math.sin(2 * math.pi * 440 * i / sample_rate))
            frames += int(value).to_bytes(2, byteorder="little", signed=True)
        with wave.open(str(wav_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(bytes(frames))
        lines.append(f"- 샘플 음성 파일 생성: {wav_path.name}")

    text = "\n".join(lines)
    print(text)
    out_file = save_output("class160_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
