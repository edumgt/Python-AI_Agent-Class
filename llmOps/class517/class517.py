# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class517 launcher
"""
from __future__ import annotations
import os, runpy
from pathlib import Path
HERE = Path(__file__).resolve().parent
CLASS_ID = Path(__file__).resolve().stem
if __name__ == "__main__":
    target = (os.getenv("CLASS_RUN_TARGET") or "example").strip().lower()
    mapping = {"example": f"{CLASS_ID}_example1.py", "solution": f"{CLASS_ID}_solution.py"}
    file_name = mapping.get(target)
    if file_name is None:
        raise SystemExit("Unknown CLASS_RUN_TARGET (use example/solution)")
    py_file = HERE / file_name
    if not py_file.exists():
        raise SystemExit(f"Run target not found: {py_file}")
    runpy.run_path(str(py_file), run_name="__main__")
