# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTICE = "이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다"

COMMENT_BY_SUFFIX = {
    ".py": "# {text}",
    ".md": "<!-- {text} -->",
    ".html": "<!-- {text} -->",
    ".sh": "# {text}",
    ".bat": "REM {text}",
    ".ps1": "# {text}",
    ".yml": "# {text}",
    ".yaml": "# {text}",
    ".txt": "# {text}",
    ".csv": "# {text}",
}

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def build_notice_line(path: Path) -> str | None:
    fmt = COMMENT_BY_SUFFIX.get(path.suffix.lower())
    if fmt is None:
        return None
    return fmt.format(text=NOTICE)


def insert_notice(path: Path, notice_line: str) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False

    if NOTICE in text:
        return False

    newline = "\r\n" if "\r\n" in text else "\n"

    # Keep shebang or cmd header first when needed.
    if path.suffix.lower() in {".py", ".sh"} and text.startswith("#!"):
        first_line_end = text.find("\n")
        if first_line_end == -1:
            updated = text + newline + notice_line + newline
        else:
            first = text[: first_line_end + 1]
            rest = text[first_line_end + 1 :]
            updated = first + notice_line + newline + rest
    elif path.suffix.lower() == ".bat" and text.lower().startswith("@echo off"):
        first_line_end = text.find("\n")
        if first_line_end == -1:
            updated = text + newline + notice_line + newline
        else:
            first = text[: first_line_end + 1]
            rest = text[first_line_end + 1 :]
            updated = first + notice_line + newline + rest
    else:
        updated = notice_line + newline + text

    path.write_text(updated, encoding="utf-8", newline="")
    return True


def apply_notice() -> None:
    changed = 0
    checked = 0

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        notice_line = build_notice_line(path)
        if notice_line is None:
            continue

        checked += 1
        if insert_notice(path, notice_line):
            changed += 1

    print(f"Checked files: {checked}")
    print(f"Updated files: {changed}")


if __name__ == "__main__":
    apply_notice()
