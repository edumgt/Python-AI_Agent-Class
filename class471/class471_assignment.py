"""
class471 assignment dispatcher

사용법:
  - 기본(입문):      python class471_assignment.py
  - 심화(advanced):  CLASS_TIER=advanced python class471_assignment.py
  - 챌린지:          CLASS_TIER=challenge python class471_assignment.py

Windows PowerShell:
  $env:CLASS_TIER="advanced"; python .\class471\class471_assignment.py
"""

from __future__ import annotations
import os, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
tier = (os.getenv("CLASS_TIER") or "basic").strip().lower()

mapping = {
    "basic": "class471_assignment_basic.py",
    "beginner": "class471_assignment_basic.py",
    "advanced": "class471_assignment_advanced.py",
    "adv": "class471_assignment_advanced.py",
    "challenge": "class471_assignment_challenge.py",
    "hard": "class471_assignment_challenge.py",
}

target = mapping.get(tier)
if not target:
    raise SystemExit(f"Unknown CLASS_TIER={tier} (use basic/advanced/challenge)")

runpy.run_path(str(HERE / target), run_name="__main__")
