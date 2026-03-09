# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class041 example1: 데이터 분석 환경 구성 · 단계 1/4 입문 이해 [class041]"""

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

if __name__ == "__main__":
    main()
