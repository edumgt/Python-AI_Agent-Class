# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class043 example1: 데이터 분석 환경 구성 · 단계 3/4 실전 검증 [class043]"""

TOPIC = "데이터 분석 환경 구성 · 단계 3/4 실전 검증 [class043]"
EXAMPLE_TEMPLATE = "dev_setup"
EXAMPLE_VARIANT = 1

from pathlib import Path
import platform

def build_setup_plan():
    plan = [
        ("venv", "python -m venv .venv"),
        ("activate", "source .venv/bin/activate"),
        ("deps", "pip install -r requirements.txt"),
        ("run", "python class043_example1.py"),
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

if __name__ == "__main__":
    main()
