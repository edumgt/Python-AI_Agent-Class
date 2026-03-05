"""
class228 advanced practice script
교과구분: 정규교과-5
교과목명: 음성 데이터 활용한 TTS와 STT 모델 개발
차시 주제: 음성 AI 개요
교육일차: Day 29
일일 교시: 4교시 (1일 8시간 운영 기준)
난이도: 입문
실행 방법:
    python class228.py
"""

from __future__ import annotations

from pathlib import Path
import math
import statistics
from textwrap import shorten


CLASS_ID = "CLASS228"
SUBJECT = "음성 데이터 활용한 TTS와 STT 모델 개발"
MODULE = "음성 AI 개요"
DAY = "Day 29"
SLOT = "4교시"
SESSION = 4


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
    practice_text = "안녕하세요. 이것은 TTS와 STT 수업용 연습 문장입니다."
    lines = [
        "음성 모델 파이프라인 실습",
        f"- 입력 문장: {practice_text}",
        "- 단계1: 텍스트 정제",
        f"  -> {practice_text.strip()}",
        "- 단계2: 음성 합성/인식용 요청 객체 구성",
    ]

    payload = {
        "text": practice_text,
        "speaker": "default",
        "language": "ko-KR",
        "session": SESSION,
    }
    lines.append(f"  -> {payload}")

    try:
        import pyttsx3
        engine = pyttsx3.init()
        out_dir = Path(__file__).resolve().parent / "outputs"
        out_dir.mkdir(exist_ok=True)
        audio_path = out_dir / "class228_tts.wav"
        engine.save_to_file(practice_text, str(audio_path))
        engine.runAndWait()
        lines.append(f"- TTS 파일 저장: {audio_path.name}")
    except Exception as e:
        lines.append(f"- TTS 저장은 선택사항(라이브러리 없음 또는 환경 제약): {type(e).__name__}")

    text = "\n".join(lines)
    print(text)
    out_file = save_output("class228_result.txt", text)
    print(f"\n산출물 저장: {out_file}")

def main():
    print_header()
    run_practice()


if __name__ == "__main__":
    main()
