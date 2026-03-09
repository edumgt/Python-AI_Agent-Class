#!/usr/bin/env bash
# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ $# -eq 0 ]; then
  echo "Usage: ./run_class.sh class001 (or project001)"
  exit 1
fi
CLASS_ID="$1"
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

CLASS_DIR="$("$PYTHON_BIN" - "$ROOT_DIR" "$CLASS_ID" <<'PY'
import csv
import sys
from pathlib import Path

root = Path(sys.argv[1])
class_id = sys.argv[2]
index_file = root / "curriculum_index.csv"

if index_file.exists():
    with index_file.open(encoding="utf-8-sig", newline="") as fp:
        rows = csv.DictReader(line for line in fp if line.strip() and not line.lstrip().startswith("#"))
        for row in rows:
            row = {str(k).lstrip("\ufeff"): v for k, v in row.items()}
            if (row.get("class") or "").strip() == class_id:
                md_file = (row.get("md_file") or "").strip()
                if md_file:
                    print((root / Path(md_file).parent).as_posix())
                    raise SystemExit(0)
                break

print((root / class_id).as_posix())
PY
)"

PY_FILE="${CLASS_DIR}/${CLASS_ID}.py"
if [ ! -f "$PY_FILE" ]; then
  echo "Class file not found: $PY_FILE"
  exit 1
fi
"$PYTHON_BIN" "$PY_FILE"
