# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
project019 assignment dispatcher

사용법:
  - 기본(입문):      python project019_assignment.py
  - 심화(advanced):  CLASS_TIER=advanced python project019_assignment.py
  - 챌린지:          CLASS_TIER=challenge python project019_assignment.py

Windows PowerShell:
  $env:CLASS_TIER="advanced"; python .\project019\project019_assignment.py
"""

from __future__ import annotations
import os, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
tier = (os.getenv("CLASS_TIER") or "basic").strip().lower()

mapping = {
    "basic": "project019_assignment_basic.py",
    "beginner": "project019_assignment_basic.py",
    "advanced": "project019_assignment_advanced.py",
    "adv": "project019_assignment_advanced.py",
    "challenge": "project019_assignment_challenge.py",
    "hard": "project019_assignment_challenge.py",
}

target = mapping.get(tier)
if not target:
    raise SystemExit(f"Unknown CLASS_TIER={tier} (use basic/advanced/challenge)")

runpy.run_path(str(HERE / target), run_name="__main__")
