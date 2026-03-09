# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class110 launcher
- 기본 실행: class110_example1.py
- 과제 실행: class110_assignment.py
- 정답 실행: class110_solution.py
"""
from __future__ import annotations

import os
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLASS_ID = Path(__file__).resolve().stem

if __name__ == "__main__":
    target = (os.getenv("CLASS_RUN_TARGET") or "example").strip().lower()
    mapping = {
        "example": f"{CLASS_ID}_example1.py",
        "assignment": f"{CLASS_ID}_assignment.py",
        "solution": f"{CLASS_ID}_solution.py",
    }
    file_name = mapping.get(target)
    if file_name is None:
        raise SystemExit("Unknown CLASS_RUN_TARGET (use example/assignment/solution)")

    py_file = HERE / file_name
    if not py_file.exists() and target == "example":
        # 예제 파일이 없으면 기존 과제 실행으로 안전하게 폴백
        py_file = HERE / f"{CLASS_ID}_assignment.py"

    if not py_file.exists():
        raise SystemExit(f"Run target not found: {py_file}")

    runpy.run_path(str(py_file), run_name="__main__")
