"""
class331 assignment dispatcher

사용법:
  - 기본(입문):      python class331_assignment.py
  - 심화(advanced):  CLASS_TIER=advanced python class331_assignment.py
  - 챌린지:          CLASS_TIER=challenge python class331_assignment.py

Windows PowerShell:
  $env:CLASS_TIER="advanced"; python .\class331\class331_assignment.py
"""

from __future__ import annotations
import os, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
tier = (os.getenv("CLASS_TIER") or "basic").strip().lower()

mapping = {
    "basic": "class331_assignment_basic.py",
    "beginner": "class331_assignment_basic.py",
    "advanced": "class331_assignment_advanced.py",
    "adv": "class331_assignment_advanced.py",
    "challenge": "class331_assignment_challenge.py",
    "hard": "class331_assignment_challenge.py",
}

target = mapping.get(tier)
if not target:
    raise SystemExit(f"Unknown CLASS_TIER={tier} (use basic/advanced/challenge)")

runpy.run_path(str(HERE / target), run_name="__main__")
