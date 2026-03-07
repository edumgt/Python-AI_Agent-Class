#!/usr/bin/env bash
# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

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

for n in $(seq 1 500); do
  CLASS_ID=$(printf "class%03d" "$n")
  CLASS_DIR="${ROOT_DIR}/${CLASS_ID}"
  NOTES_FILE="${CLASS_DIR}/instructor_notes.md"

  if [ ! -f "$NOTES_FILE" ]; then
    continue
  fi

  if grep -qE "Day[[:space:]]+${DAY}\\b" "$NOTES_FILE"; then
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
    python "$PY_FILE"
    echo
  fi
done