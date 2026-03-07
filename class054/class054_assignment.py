# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""
class054 assignment dispatcher

사용법:
  - 기본(입문):      python class054_assignment.py
  - 심화(advanced):  CLASS_TIER=advanced python class054_assignment.py
  - 챌린지:          CLASS_TIER=challenge python class054_assignment.py

Windows PowerShell:
  $env:CLASS_TIER="advanced"; python .\class054\class054_assignment.py
"""

from __future__ import annotations
import os, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
tier = (os.getenv("CLASS_TIER") or "basic").strip().lower()

mapping = {
    "basic": "class054_assignment_basic.py",
    "beginner": "class054_assignment_basic.py",
    "advanced": "class054_assignment_advanced.py",
    "adv": "class054_assignment_advanced.py",
    "challenge": "class054_assignment_challenge.py",
    "hard": "class054_assignment_challenge.py",
}

target = mapping.get(tier)
if not target:
    raise SystemExit(f"Unknown CLASS_TIER={tier} (use basic/advanced/challenge)")

runpy.run_path(str(HERE / target), run_name="__main__")
