# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class033 example2: Python 외부 라이브러리 활용 · 단계 1/2 입문 이해 [class033]"""

TOPIC = "Python 외부 라이브러리 활용 · 단계 1/2 입문 이해 [class033]"
EXAMPLE_TEMPLATE = "module_package"
EXAMPLE_VARIANT = 2

import importlib.util
import math
import os
import random
from datetime import datetime
from pathlib import Path

def ensure_user_module():
    module_path = Path(__file__).with_name("class033_user_module.py")
    if not module_path.exists():
        module_path.write_text(
            "def build_message(name):\n"
            "    return f'hello, {name}'\n",
            encoding="utf-8",
        )
    spec = importlib.util.spec_from_file_location("user_module", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module, module_path

def stdlib_snapshot(seed):
    random.seed(seed)
    return {
        "randint": random.randint(1, 100),
        "sqrt_81": int(math.sqrt(81)),
        "today": datetime.now().strftime("%Y-%m-%d"),
        "cwd_name": os.path.basename(os.getcwd()),
    }

def build_test_cases():
    cases = [("baseline", 7)]
    if EXAMPLE_VARIANT >= 2:
        cases.append(("alt_seed", 21))
    if EXAMPLE_VARIANT >= 3:
        cases.append(("seed_42", 42))
    if EXAMPLE_VARIANT >= 4:
        cases.append(("seed_99", 99))
    if EXAMPLE_VARIANT >= 5:
        cases.append(("seed_123", 123))
    return cases

def main():
    print("오늘 주제:", TOPIC)
    user_module, module_path = ensure_user_module()
    reports = []
    for case_name, seed in build_test_cases():
        snap = stdlib_snapshot(seed)
        snap["case"] = case_name
        snap["message"] = user_module.build_message(case_name)
        snap["module_file"] = module_path.name
        reports.append(snap)
        print(f"[{case_name}] 모듈 리포트:", snap)
    return {"variant": EXAMPLE_VARIANT, "case_count": len(reports), "module": module_path.name}

def extension_mission():
    return {
        "mission": "random/math/datetime/os 호출 결과를 한 리포트로 묶으세요.",
        "check": "사용자 정의 모듈 import 실패/성공 케이스를 모두 확인하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
