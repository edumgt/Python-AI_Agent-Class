# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class041 example3: 데이터 분석 환경 구성 · 단계 1/4 입문 이해 [class041]"""

TOPIC = "데이터 분석 환경 구성 · 단계 1/4 입문 이해 [class041]"
EXAMPLE_TEMPLATE = "dev_setup"

from pathlib import Path
import platform

def build_setup_plan():
    return [
        ("venv", "python -m venv .venv"),
        ("activate", "source .venv/bin/activate"),
        ("deps", "pip install -r requirements.txt"),
        ("run", "python class041_example.py"),
    ]

def scan_workspace():
    root = Path(__file__).resolve().parents[2]
    return {
        "platform": platform.system(),
        "requirements_exists": (root / "requirements.txt").exists(),
        "readme_exists": (root / "README.md").exists(),
    }

def main():
    print("오늘 주제:", TOPIC)
    plan = build_setup_plan()
    for idx, (name, cmd) in enumerate(plan, start=1):
        print(f"{idx}. {name} -> {cmd}")
    status = scan_workspace()
    print("환경 점검:", status)
    return {"step_count": len(plan), **status}

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "핵심 함수를 재사용 가능한 모듈로 분리하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
