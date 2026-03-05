"""
class099 assignment dispatcher

사용법:
  - 기본(입문):      python class099_assignment.py
  - 심화(advanced):  CLASS_TIER=advanced python class099_assignment.py
  - 챌린지:          CLASS_TIER=challenge python class099_assignment.py

Windows PowerShell:
  $env:CLASS_TIER="advanced"; python .\class099\class099_assignment.py
"""

from __future__ import annotations
import os, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
tier = (os.getenv("CLASS_TIER") or "basic").strip().lower()

mapping = {
    "basic": "class099_assignment_basic.py",
    "beginner": "class099_assignment_basic.py",
    "advanced": "class099_assignment_advanced.py",
    "adv": "class099_assignment_advanced.py",
    "challenge": "class099_assignment_challenge.py",
    "hard": "class099_assignment_challenge.py",
}

target = mapping.get(tier)
if not target:
    raise SystemExit(f"Unknown CLASS_TIER={tier} (use basic/advanced/challenge)")

runpy.run_path(str(HERE / target), run_name="__main__")
