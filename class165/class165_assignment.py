"""
class165 assignment dispatcher

사용법:
  - 기본(입문):      python class165_assignment.py
  - 심화(advanced):  CLASS_TIER=advanced python class165_assignment.py
  - 챌린지:          CLASS_TIER=challenge python class165_assignment.py

Windows PowerShell:
  $env:CLASS_TIER="advanced"; python .\class165\class165_assignment.py
"""

from __future__ import annotations
import os, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
tier = (os.getenv("CLASS_TIER") or "basic").strip().lower()

mapping = {
    "basic": "class165_assignment_basic.py",
    "beginner": "class165_assignment_basic.py",
    "advanced": "class165_assignment_advanced.py",
    "adv": "class165_assignment_advanced.py",
    "challenge": "class165_assignment_challenge.py",
    "hard": "class165_assignment_challenge.py",
}

target = mapping.get(tier)
if not target:
    raise SystemExit(f"Unknown CLASS_TIER={tier} (use basic/advanced/challenge)")

runpy.run_path(str(HERE / target), run_name="__main__")
