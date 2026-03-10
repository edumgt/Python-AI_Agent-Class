# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class001 example3: 수업 준비 1: 필수 플랫폼 가입/계정 설정 (class001) · 단계 1/1 입문 이해 [class001]"""

TOPIC = "수업 준비 1: 필수 플랫폼 가입/계정 설정 (class001) · 단계 1/1 입문 이해 [class001]"
EXAMPLE_TEMPLATE = "dev_setup"
EXAMPLE_VARIANT = 3

from pathlib import Path
import platform

def build_setup_plan():
    plan = [
        ("venv", "python -m venv .venv"),
        ("activate", "source .venv/bin/activate"),
        ("deps", "pip install -r requirements.txt"),
        ("run", "python class001_example1.py"),
    ]
    if EXAMPLE_VARIANT >= 3:
        plan.append(("freeze", "pip freeze > requirements.lock.txt"))
    if EXAMPLE_VARIANT >= 4:
        plan.append(("smoke", "python -c \"import numpy, pandas\""))
    if EXAMPLE_VARIANT >= 5:
        plan.append(("check", "python -m pip check"))
    return plan

def build_path_checks():
    checks = ["README.md", "requirements.txt"]
    if EXAMPLE_VARIANT >= 2:
        checks.append("curriculum_index.csv")
    if EXAMPLE_VARIANT >= 3:
        checks.extend(["dataVizPrep", "tools/rebuild_examples_and_validate.py"])
    if EXAMPLE_VARIANT >= 4:
        checks.append("run_class.sh")
    if EXAMPLE_VARIANT >= 5:
        checks.append("run_day.sh")
    return checks

def scan_workspace():
    root = Path(__file__).resolve().parents[2]
    checks = build_path_checks()
    existing = {rel: (root / rel).exists() for rel in checks}
    return {
        "platform": platform.system(),
        "variant": EXAMPLE_VARIANT,
        "requirements_exists": (root / "requirements.txt").exists(),
        "readme_exists": (root / "README.md").exists(),
        "checks": existing,
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
        "task": "requirements.lock.txt 생성 자동화 스크립트를 추가하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
