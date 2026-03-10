# This file is generated as part of the class web practice environment.

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

APP_DIR = Path(__file__).resolve().parent
CLASS_ID = APP_DIR.name if re.fullmatch(r"class\d+", APP_DIR.name) else "class"
CLIENT_FILE = APP_DIR / "client.html"
TIMEOUT_SECONDS = 20

app = FastAPI(title=f"{CLASS_ID} Web Practice Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    example: int


def parse_topic_from_file(example_file: Path) -> str:
    try:
        for line in example_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("TOPIC = "):
                raw = line.split("=", 1)[1].strip()
                return raw.strip('"').strip("'")
    except Exception:
        return ""
    return ""


def list_examples() -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    pattern = re.compile(rf"^{re.escape(CLASS_ID)}_example(\d+)\.py$")
    for path in sorted(APP_DIR.glob(f"{CLASS_ID}_example*.py")):
        m = pattern.fullmatch(path.name)
        if not m:
            continue
        idx = int(m.group(1))
        items.append(
            {
                "index": idx,
                "file": path.name,
                "topic": parse_topic_from_file(path),
            }
        )
    return items


def find_example_file(example_index: int) -> Path:
    target = APP_DIR / f"{CLASS_ID}_example{example_index}.py"
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"Example {example_index} not found")
    return target


def run_python_file(path: Path) -> dict[str, object]:
    try:
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(APP_DIR),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "exit_code": None,
            "stdout": (exc.stdout or "").strip(),
            "stderr": f"Execution timed out after {TIMEOUT_SECONDS} seconds.",
            "timed_out": True,
        }

    return {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "timed_out": False,
    }


@app.get("/")
def root() -> FileResponse:
    if not CLIENT_FILE.exists():
        raise HTTPException(status_code=404, detail="client.html not found")
    return FileResponse(CLIENT_FILE)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "class": CLASS_ID}


@app.get("/api/meta")
def meta() -> dict[str, object]:
    examples = list_examples()
    topic = examples[0]["topic"] if examples else ""
    return {
        "class_id": CLASS_ID,
        "class_dir": str(APP_DIR.name),
        "topic": topic,
        "example_count": len(examples),
        "examples": examples,
    }


@app.get("/api/source/{example_index}")
def source(example_index: int) -> JSONResponse:
    file_path = find_example_file(example_index)
    try:
        source_code = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to decode source: {exc}") from exc

    return JSONResponse(
        {
            "class_id": CLASS_ID,
            "example": example_index,
            "file": file_path.name,
            "source": source_code,
        }
    )


@app.post("/api/run")
def run_example(payload: RunRequest) -> JSONResponse:
    file_path = find_example_file(payload.example)
    result = run_python_file(file_path)
    return JSONResponse(
        {
            "class_id": CLASS_ID,
            "example": payload.example,
            "file": file_path.name,
            **result,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
