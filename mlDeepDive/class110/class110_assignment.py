# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class110 assignment dispatcher

사용법:
  - 기본(입문):      python class110_assignment.py
  - 심화(advanced):  CLASS_TIER=advanced python class110_assignment.py
  - 챌린지:          CLASS_TIER=challenge python class110_assignment.py

Windows PowerShell:
  $env:CLASS_TIER="advanced"; python .\class110\class110_assignment.py
"""

from __future__ import annotations
import os, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
tier = (os.getenv("CLASS_TIER") or "basic").strip().lower()

mapping = {
    "basic": "class110_assignment_basic.py",
    "beginner": "class110_assignment_basic.py",
    "advanced": "class110_assignment_advanced.py",
    "adv": "class110_assignment_advanced.py",
    "challenge": "class110_assignment_challenge.py",
    "hard": "class110_assignment_challenge.py",
}

target = mapping.get(tier)
if not target:
    raise SystemExit(f"Unknown CLASS_TIER={tier} (use basic/advanced/challenge)")

runpy.run_path(str(HERE / target), run_name="__main__")
