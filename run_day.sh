#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ $# -eq 0 ]; then
  echo "Usage: ./run_day.sh 1"
  exit 1
fi
DAY=$(printf "%02d" "$1")
for n in $(seq 1 500); do
  CLASS_ID=$(printf "class%03d" "$n")
  PY_FILE="${ROOT_DIR}/${CLASS_ID}/${CLASS_ID}.py"
  if grep -q "교육일차: Day ${DAY}" "$PY_FILE"; then
    echo "========== ${CLASS_ID} =========="
    python "$PY_FILE"
    echo
  fi
done
