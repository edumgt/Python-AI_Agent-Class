"""
class317 launcher
- 과제: class317_assignment.py
- 정답: class317_solution.py
"""
from __future__ import annotations

import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    # 기본 실행은 과제(assignment)로 연결
    runpy.run_path(str(HERE / "class317_assignment.py"), run_name="__main__")
