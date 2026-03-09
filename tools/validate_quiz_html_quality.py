# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"


def read_rows() -> list[dict[str, str]]:
    with INDEX_FILE.open(encoding="utf-8-sig", newline="") as fp:
        lines = [line for line in fp if line.strip() and not line.lstrip().startswith("#")]
        raw_rows = list(csv.DictReader(lines))
    return [{str(k).lstrip("\ufeff"): v for k, v in row.items()} for row in raw_rows]


def class_dir_from_row(row: dict[str, str]) -> Path:
    md_rel = (row.get("md_file") or "").strip()
    if md_rel:
        md_path = ROOT / Path(md_rel)
        if md_path.name:
            return md_path.parent
    return ROOT / row["class"]


def expected_example_files(class_dir: Path, class_id: str) -> list[str]:
    files: list[tuple[int, str]] = []
    for path in class_dir.glob(f"{class_id}_example*.py"):
        match = re.match(rf"^{re.escape(class_id)}_example(\d+)\.py$", path.name, flags=re.IGNORECASE)
        if not match:
            continue
        files.append((int(match.group(1)), path.name))
    files.sort(key=lambda item: item[0])
    if files:
        return [name for _, name in files]

    legacy = class_dir / f"{class_id}_example.py"
    if legacy.exists():
        return [f"{class_id}_example1.py"]
    return []


def extract_quiz_payload_from_html(text: str) -> dict[str, Any]:
    marker = "const QUIZ_DATA ="
    marker_index = text.find(marker)
    if marker_index < 0:
        raise ValueError("QUIZ_DATA marker not found")

    start = text.find("{", marker_index)
    if start < 0:
        raise ValueError("quiz json start brace not found")

    depth = 0
    in_string = False
    escape = False
    end = -1

    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue
        if ch == "{":
            depth += 1
            continue
        if ch == "}":
            depth -= 1
            if depth == 0:
                end = i
                break

    if end < 0:
        raise ValueError("quiz json end brace not found")

    return json.loads(text[start : end + 1])


def validate_quiz_payload(row: dict[str, str], payload: dict[str, Any], expected_files: list[str]) -> list[str]:
    class_id = row["class"]
    module = row["module"]
    errors: list[str] = []

    if payload.get("class_id") != class_id:
        errors.append(f"class_id mismatch: {payload.get('class_id')} != {class_id}")
    if payload.get("module") != module:
        errors.append("module mismatch")

    questions = payload.get("questions")
    if not isinstance(questions, list):
        errors.append("questions is not a list")
        return errors

    if payload.get("question_count") != 10:
        errors.append(f"question_count is {payload.get('question_count')}, expected 10")
    if len(questions) != 10:
        errors.append(f"questions length is {len(questions)}, expected 10")

    for i, q in enumerate(questions, start=1):
        if not isinstance(q, dict):
            errors.append(f"q{i} is not object")
            continue
        options = q.get("options")
        answer_index = q.get("answer_index")
        if not isinstance(options, list) or len(options) != 4:
            errors.append(f"q{i} options length is {len(options) if isinstance(options, list) else 'invalid'}, expected 4")
        if not isinstance(answer_index, int):
            errors.append(f"q{i} answer_index is not int")
        elif isinstance(options, list) and not (0 <= answer_index < len(options)):
            errors.append(f"q{i} answer_index out of range")

    if questions:
        q1 = questions[0]
        if isinstance(q1, dict):
            options = q1.get("options", [])
            answer_index = q1.get("answer_index", -1)
            if isinstance(options, list) and isinstance(answer_index, int) and 0 <= answer_index < len(options):
                if options[answer_index] != module:
                    errors.append("q1 correct answer is not module")
            else:
                errors.append("q1 answer validation failed")

    ref = payload.get("example_reference") or {}
    ref_files = ref.get("files") if isinstance(ref, dict) else []
    if not isinstance(ref_files, list):
        ref_files = []
    if ref_files != expected_files:
        errors.append(f"example_reference.files mismatch: expected={expected_files}, got={ref_files}")

    snippet_files = []
    snippets = payload.get("example_snippets")
    if isinstance(snippets, list):
        for item in snippets:
            if isinstance(item, dict) and isinstance(item.get("file"), str):
                snippet_files.append(item["file"])
    expected_snippet_files = expected_files[:5]
    if snippet_files != expected_snippet_files:
        errors.append(f"example_snippets files mismatch: expected={expected_snippet_files}, got={snippet_files}")

    if expected_snippet_files:
        chunks: list[str] = []
        for q in questions:
            if not isinstance(q, dict):
                continue
            question_text = q.get("question")
            if isinstance(question_text, str):
                chunks.append(question_text)
            options = q.get("options")
            if isinstance(options, list):
                chunks.extend(str(opt) for opt in options)
            explanation = q.get("explanation")
            if isinstance(explanation, str):
                chunks.append(explanation)
        text_blob = "\n".join(chunks)
        missing_refs = [name for name in expected_snippet_files if name not in text_blob]
        if missing_refs:
            errors.append(f"questions do not reference files: {', '.join(missing_refs)}")

    return errors


def main() -> int:
    rows = read_rows()
    checked = 0
    all_errors: list[str] = []

    for row in rows:
        class_id = row["class"]
        class_dir = class_dir_from_row(row)
        quiz_path = class_dir / f"{class_id}_quiz.html"
        checked += 1

        if not quiz_path.exists():
            all_errors.append(f"{class_id}: quiz file missing")
            continue

        try:
            text = quiz_path.read_text(encoding="utf-8")
        except Exception as exc:
            all_errors.append(f"{class_id}: quiz read failed: {type(exc).__name__}: {exc}")
            continue

        try:
            payload = extract_quiz_payload_from_html(text)
        except Exception as exc:
            all_errors.append(f"{class_id}: quiz payload parse failed: {type(exc).__name__}: {exc}")
            continue

        expected_files = expected_example_files(class_dir, class_id)
        errors = validate_quiz_payload(row, payload, expected_files)
        for err in errors:
            all_errors.append(f"{class_id}: {err}")

    print(f"checked={checked}")
    print(f"errors={len(all_errors)}")
    for item in all_errors[:120]:
        print(f"- {item}")
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
