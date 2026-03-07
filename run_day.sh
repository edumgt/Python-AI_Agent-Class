#!/usr/bin/env bash
# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

if [ $# -eq 0 ]; then
  echo "Usage: ./run_day.sh 1 [solution|launcher|assignment|basic|advanced|challenge]"
  exit 1
fi

DAY=$(printf "%02d" "$1")
TARGET="${2:-solution}"

case "$TARGET" in
  solution|launcher|assignment|basic|advanced|challenge) ;;
  *)
    echo "Unknown target: $TARGET"
    echo "Use one of: solution, launcher, assignment, basic, advanced, challenge"
    exit 1
    ;;
esac

"$PYTHON_BIN" - "$ROOT_DIR" "$DAY" <<'PY' | while IFS='|' read -r CLASS_ID CLASS_DIR; do
import csv
import sys
from pathlib import Path

root = Path(sys.argv[1])
target_day = sys.argv[2]
index_file = root / "curriculum_index.csv"

if not index_file.exists():
    raise SystemExit(0)

with index_file.open(encoding="utf-8-sig", newline="") as fp:
    rows = csv.DictReader(line for line in fp if line.strip() and not line.lstrip().startswith("#"))
    for row in rows:
        row = {str(k).lstrip("\ufeff"): v for k, v in row.items()}
        class_id = (row.get("class") or "").strip()
        day = str((row.get("day") or "")).strip()
        md_file = (row.get("md_file") or "").strip()
        if not class_id or not day:
            continue
        if day.zfill(2) != target_day:
            continue
        if md_file:
            class_dir = root / Path(md_file).parent
        else:
            class_dir = root / class_id
        print(f"{class_id}|{class_dir.as_posix()}")
PY
  case "$TARGET" in
    solution) PY_FILE="${CLASS_DIR}/${CLASS_ID}_solution.py" ;;
    launcher) PY_FILE="${CLASS_DIR}/${CLASS_ID}.py" ;;
    assignment) PY_FILE="${CLASS_DIR}/${CLASS_ID}_assignment.py" ;;
    basic) PY_FILE="${CLASS_DIR}/${CLASS_ID}_assignment_basic.py" ;;
    advanced) PY_FILE="${CLASS_DIR}/${CLASS_ID}_assignment_advanced.py" ;;
    challenge) PY_FILE="${CLASS_DIR}/${CLASS_ID}_assignment_challenge.py" ;;
  esac

  if [ ! -f "$PY_FILE" ]; then
    echo "Skip ${CLASS_ID}: file not found (${PY_FILE})"
    continue
  fi

  echo "========== ${CLASS_ID} (${TARGET}) =========="
  "$PYTHON_BIN" "$PY_FILE"
  echo
done
