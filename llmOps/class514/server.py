# This file is generated as part of the class web practice environment.
from __future__ import annotations
import re, subprocess, sys
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
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class RunRequest(BaseModel):
    target: str = "example"

@app.get("/")
async def root():
    if CLIENT_FILE.exists():
        return FileResponse(CLIENT_FILE)
    return JSONResponse({"class": CLASS_ID, "status": "ok"})

@app.post("/run")
async def run_example(req: RunRequest):
    allowed = {"example", "solution"}
    if req.target not in allowed:
        raise HTTPException(status_code=400, detail="Invalid target")
    py_file = APP_DIR / f"{CLASS_ID}_{req.target}1.py"
    if not py_file.exists():
        raise HTTPException(status_code=404, detail=f"{py_file.name} not found")
    try:
        result = subprocess.run(
            [sys.executable, str(py_file)],
            capture_output=True, text=True, timeout=TIMEOUT_SECONDS
        )
        return JSONResponse({"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode})
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Execution timed out")

@app.get("/source/{filename}")
async def get_source(filename: str):
    if not re.fullmatch(r"[\w]+\.py", filename):
        raise HTTPException(status_code=400, detail="Invalid filename")
    src = APP_DIR / filename
    if not src.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return JSONResponse({"filename": filename, "content": src.read_text(encoding="utf-8")})
