#!/usr/bin/env bash
# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ $# -eq 0 ]; then
  echo "Usage: ./run_class.sh class001"
  exit 1
fi
CLASS_ID="$1"
PY_FILE="${ROOT_DIR}/${CLASS_ID}/${CLASS_ID}.py"
if [ ! -f "$PY_FILE" ]; then
  echo "Class file not found: $PY_FILE"
  exit 1
fi
python "$PY_FILE"
