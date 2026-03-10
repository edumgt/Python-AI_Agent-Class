# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import csv
import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"
PROJECT_ROOT = ROOT / "project"


def load_project_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with INDEX_FILE.open(encoding="utf-8-sig", newline="") as fp:
        reader = csv.DictReader(line for line in fp if line.strip() and not line.lstrip().startswith("#"))
        for raw in reader:
            row = {str(k).lstrip("\ufeff"): (v or "") for k, v in raw.items()}
            class_id = row.get("class", "").strip()
            if class_id.startswith("project"):
                rows.append(row)
    rows.sort(key=lambda r: r["class"])
    return rows


def project_name_from_md_file(md_file: str) -> str:
    parts = Path(md_file).parts
    if len(parts) >= 2 and parts[0] == "project" and parts[1].startswith("Prj_"):
        return parts[1]
    return "Prj_Project"


def class_dir_from_row(row: dict[str, str]) -> Path:
    md_file = (row.get("md_file") or "").strip()
    if md_file:
        return ROOT / Path(md_file).parent
    return PROJECT_ROOT / "Prj_PersonaVoiceAI" / row["class"].strip()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def slug_from_prj_name(prj_name: str) -> str:
    slug = prj_name.replace("Prj_", "").strip()
    out = []
    for ch in slug:
        if ch.isalnum():
            out.append(ch.lower())
        else:
            out.append("-")
    clean = "".join(out)
    while "--" in clean:
        clean = clean.replace("--", "-")
    return clean.strip("-") or "project"


def topic_from_module(module: str) -> str:
    # Remove trailing [projectXXX] in docs title.
    if "[project" in module:
        return module.split("[project", 1)[0].strip()
    return module.strip()


def build_core_py(track_code: str) -> str:
    return dedent(
        f"""\
        from __future__ import annotations

        from dataclasses import dataclass
        from datetime import datetime, timezone
        from pathlib import Path
        import json
        import statistics


        @dataclass
        class ScenarioResult:
            track: str
            status: str
            summary: dict


        def _safe_mean(values: list[float]) -> float:
            return float(statistics.fmean(values)) if values else 0.0


        def _safe_stdev(values: list[float]) -> float:
            if len(values) < 2:
                return 0.0
            return float(statistics.pstdev(values))


        def evaluate(track_code: str, values: list[float], note: str) -> ScenarioResult:
            values = [float(v) for v in values]
            avg = _safe_mean(values)
            std = _safe_stdev(values)

            if track_code == "프로젝트-1":
                profile_score = max(0.0, min(100.0, round(avg * 100, 2)))
                style_consistency = max(0.0, min(100.0, round((1.0 - std) * 100, 2)))
                status = "ready" if profile_score >= 70 else "design"
                summary = {{
                    "phase": "개인 맞춤 코칭 음성봇 기초 구축",
                    "profile_score": profile_score,
                    "style_consistency": style_consistency,
                    "note": note,
                }}
            elif track_code == "프로젝트-2":
                loop_quality = max(0.0, min(100.0, round((avg - std * 0.4) * 100, 2)))
                status = "stable" if loop_quality >= 68 else "tune"
                summary = {{
                    "phase": "STT-LLM-TTS 코칭 대화 파이프라인",
                    "loop_quality": loop_quality,
                    "latency_hint_ms": int((0.18 + std) * 1000),
                    "note": note,
                }}
            elif track_code == "프로젝트-3":
                dataset_quality = max(0.0, min(100.0, round((avg * 0.7 + (1.0 - std) * 0.3) * 100, 2)))
                status = "usable" if dataset_quality >= 72 else "relabel"
                summary = {{
                    "phase": "사전 데이터 기반 PERSONA AI 구축",
                    "dataset_quality": dataset_quality,
                    "label_consistency": round((1.0 - std) * 100, 2),
                    "note": note,
                }}
            else:
                drift_score = max(0.0, min(100.0, round(((1.0 - avg) + std) * 100, 2)))
                status = "retrain" if drift_score >= 35 else "monitor"
                summary = {{
                    "phase": "PERSONA AI 지속학습과 품질 운영",
                    "drift_score": drift_score,
                    "next_action": "재학습 큐 등록" if status == "retrain" else "모니터링 유지",
                    "note": note,
                }}

            return ScenarioResult(track=track_code, status=status, summary=summary)


        def append_history(history_file: Path, payload: dict) -> None:
            history_file.parent.mkdir(parents=True, exist_ok=True)
            record = {{
                "timestamp": datetime.now(timezone.utc).isoformat(),
                **payload,
            }}
            with history_file.open("a", encoding="utf-8") as fp:
                fp.write(json.dumps(record, ensure_ascii=False) + "\\n")


        def load_recent(history_file: Path, limit: int = 20) -> list[dict]:
            if not history_file.exists():
                return []
            lines = history_file.read_text(encoding="utf-8").splitlines()
            rows = []
            for line in lines[-max(1, limit):]:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
            return rows
        """
    )


def scaffold_project(row: dict[str, str]) -> None:
    project_id = row["class"].strip()
    track_code = row.get("subject_code", "").strip() or "프로젝트-1"
    module = row.get("module", "").strip()
    topic = topic_from_module(module)
    md_file = row.get("md_file", "").strip()
    prj_name = project_name_from_md_file(md_file)

    day = row.get("day", "").strip()
    slot = row.get("slot", "").strip()
    seq = row.get("subject_session", "").strip()

    project_num = int(project_id.replace("project", ""))
    host_port = 9100 + project_num
    app_root = class_dir_from_row(row)

    write(
        app_root / "requirements.txt",
        dedent(
            """\
            fastapi==0.116.1
            uvicorn[standard]==0.35.0
            pydantic==2.11.7
            pytest==8.4.2
            httpx==0.28.1
            """
        ),
    )

    write(
        app_root / ".dockerignore",
        dedent(
            """\
            __pycache__/
            .pytest_cache/
            .venv/
            *.pyc
            *.pyo
            *.pyd
            .git/
            """
        ),
    )

    write(
        app_root / ".env.example",
        dedent(
            f"""\
            PROJECT_ID={project_id}
            PROJECT_NAME={prj_name}
            PROJECT_TRACK={track_code}
            PROJECT_TOPIC={topic}
            APP_HOST_PORT={host_port}
            """
        ),
    )

    write(
        app_root / "Dockerfile",
        dedent(
            """\
            FROM python:3.11-slim

            ENV PYTHONDONTWRITEBYTECODE=1 \\
                PYTHONUNBUFFERED=1

            WORKDIR /app

            COPY requirements.txt /app/requirements.txt
            RUN pip install --no-cache-dir -r /app/requirements.txt

            COPY backend /app/backend
            COPY frontend /app/frontend

            EXPOSE 8080

            CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
            """
        ),
    )

    write(
        app_root / "docker-compose.yml",
        dedent(
            f"""\
            services:
              api:
                build:
                  context: .
                  dockerfile: Dockerfile
                environment:
                  PROJECT_ID: ${{PROJECT_ID:-{project_id}}}
                  PROJECT_NAME: ${{PROJECT_NAME:-{prj_name}}}
                  PROJECT_TRACK: ${{PROJECT_TRACK:-{track_code}}}
                  PROJECT_TOPIC: ${{PROJECT_TOPIC:-{topic}}}
                ports:
                  - "${{APP_HOST_PORT:-{host_port}}}:8080"
                healthcheck:
                  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2).read()"]
                  interval: 15s
                  timeout: 5s
                  retries: 5
                restart: unless-stopped
            """
        ),
    )

    write(
        app_root / "Makefile",
        dedent(
            """\
            .PHONY: run test docker-up docker-down

            run:
            	python -m uvicorn backend.app.main:app --reload --port 8080

            test:
            	python -m unittest discover -s backend/tests -p 'test_*.py'

            docker-up:
            	docker compose up -d --build

            docker-down:
            	docker compose down
            """
        ),
    )

    write(
        app_root / "backend" / "app" / "__init__.py",
        "",
    )

    write(
        app_root / "backend" / "app" / "config.py",
        dedent(
            f"""\
            from __future__ import annotations

            from dataclasses import dataclass
            import os


            @dataclass
            class Settings:
                project_id: str = os.getenv("PROJECT_ID", "{project_id}")
                project_name: str = os.getenv("PROJECT_NAME", "{prj_name}")
                project_track: str = os.getenv("PROJECT_TRACK", "{track_code}")
                project_topic: str = os.getenv("PROJECT_TOPIC", "{topic}")


            settings = Settings()
            """
        ),
    )

    write(
        app_root / "backend" / "app" / "schemas.py",
        dedent(
            """\
            from __future__ import annotations

            from pydantic import BaseModel, Field


            class RunRequest(BaseModel):
                values: list[float] = Field(default_factory=lambda: [0.2, 0.4, 0.6])
                note: str = "manual-run"


            class RunResponse(BaseModel):
                project_id: str
                status: str
                summary: dict
                history_count: int
            """
        ),
    )

    write(app_root / "backend" / "app" / "core.py", build_core_py(track_code))

    write(
        app_root / "backend" / "app" / "main.py",
        dedent(
            """\
            from __future__ import annotations

            from pathlib import Path

            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware
            from fastapi.responses import FileResponse
            from fastapi.staticfiles import StaticFiles

            from backend.app.config import settings
            from backend.app.core import append_history, evaluate, load_recent
            from backend.app.schemas import RunRequest, RunResponse


            app = FastAPI(title=f"{settings.project_id} API", version="1.0.0")

            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            PROJECT_ROOT = Path(__file__).resolve().parents[2]
            FRONTEND_DIR = PROJECT_ROOT / "frontend"
            DATA_DIR = PROJECT_ROOT / "data"
            HISTORY_FILE = DATA_DIR / "run_history.jsonl"

            if FRONTEND_DIR.exists():
                app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")


            @app.get("/")
            def home() -> FileResponse:
                return FileResponse(FRONTEND_DIR / "index.html")


            @app.get("/health")
            def health() -> dict:
                recent = load_recent(HISTORY_FILE, limit=1)
                return {
                    "status": "ok",
                    "project_id": settings.project_id,
                    "project_name": settings.project_name,
                    "track": settings.project_track,
                    "topic": settings.project_topic,
                    "history_exists": bool(recent),
                }


            @app.get("/v1/project/meta")
            def project_meta() -> dict:
                return {
                    "project_id": settings.project_id,
                    "project_name": settings.project_name,
                    "track": settings.project_track,
                    "topic": settings.project_topic,
                }


            @app.get("/v1/project/history")
            def project_history(limit: int = 20) -> dict:
                rows = load_recent(HISTORY_FILE, limit=limit)
                return {"items": rows, "count": len(rows)}


            @app.post("/v1/project/run", response_model=RunResponse)
            def project_run(payload: RunRequest) -> RunResponse:
                result = evaluate(
                    track_code=settings.project_track,
                    values=payload.values,
                    note=payload.note,
                )
                record = {
                    "project_id": settings.project_id,
                    "project_name": settings.project_name,
                    "track": result.track,
                    "status": result.status,
                    "summary": result.summary,
                }
                append_history(HISTORY_FILE, record)
                history_count = len(load_recent(HISTORY_FILE, limit=10_000))
                return RunResponse(
                    project_id=settings.project_id,
                    status=result.status,
                    summary=result.summary,
                    history_count=history_count,
                )
            """
        ),
    )

    write(
        app_root / "backend" / "tests" / "test_core.py",
        dedent(
            """\
            from __future__ import annotations

            import unittest

            from backend.app.core import evaluate


            class CoreScenarioTests(unittest.TestCase):
                def test_evaluate_returns_status(self) -> None:
                    result = evaluate(track_code="프로젝트-1", values=[0.1, 0.2, 0.3], note="unit-test")
                    self.assertIn(result.status, {"ready", "design"})
                    self.assertIsInstance(result.summary, dict)

                def test_continual_track_has_drift_score(self) -> None:
                    result = evaluate(track_code="프로젝트-4", values=[0.8, 0.9, 0.7], note="aiops")
                    self.assertIn("drift_score", result.summary)


            if __name__ == "__main__":
                unittest.main()
            """
        ),
    )

    write(
        app_root / "backend" / "tests" / "test_api.py",
        dedent(
            """\
            from __future__ import annotations

            import unittest

            try:
                from fastapi.testclient import TestClient
                from backend.app.main import app
            except Exception:
                TestClient = None
                app = None


            class ApiSmokeTests(unittest.TestCase):
                @unittest.skipIf(TestClient is None, "fastapi/testclient not installed")
                def test_health_endpoint(self) -> None:
                    client = TestClient(app)
                    resp = client.get("/health")
                    self.assertEqual(resp.status_code, 200)
                    payload = resp.json()
                    self.assertEqual(payload.get("status"), "ok")


            if __name__ == "__main__":
                unittest.main()
            """
        ),
    )

    write(
        app_root / "frontend" / "index.html",
        dedent(
            f"""\
            <!doctype html>
            <html lang="ko">
            <head>
              <meta charset="UTF-8" />
              <meta name="viewport" content="width=device-width, initial-scale=1.0" />
              <title>{project_id} - {prj_name}</title>
              <link rel="stylesheet" href="/assets/style.css" />
            </head>
            <body>
              <main class="container">
                <section class="card">
                  <h1>{project_id} · {prj_name}</h1>
                  <p class="topic">{topic}</p>
                  <p class="meta">Day {day} / {slot}교시 · 세션 {seq}</p>
                  <button id="meta-btn">프로젝트 메타 로드</button>
                  <pre id="meta-box">메타 정보를 불러오세요.</pre>
                </section>

                <section class="card">
                  <h2>시나리오 실행</h2>
                  <label>values (comma separated)</label>
                  <input id="values" value="0.2,0.4,0.6" />
                  <label>note</label>
                  <input id="note" value="frontend-run" />
                  <button id="run-btn">실행</button>
                  <pre id="run-box">실행 결과가 여기에 표시됩니다.</pre>
                </section>
              </main>

              <script src="/assets/app.js"></script>
            </body>
            </html>
            """
        ),
    )

    write(
        app_root / "frontend" / "style.css",
        dedent(
            """\
            :root {
              --bg: #f2f5f8;
              --card: #ffffff;
              --ink: #0f172a;
              --muted: #475569;
              --brand: #0ea5e9;
            }

            * { box-sizing: border-box; }

            body {
              margin: 0;
              font-family: "Noto Sans KR", "Segoe UI", sans-serif;
              background: radial-gradient(circle at top left, #e0f2fe, var(--bg));
              color: var(--ink);
              min-height: 100vh;
              display: flex;
              justify-content: center;
              align-items: flex-start;
              padding: 24px;
            }

            .container {
              width: min(920px, 100%);
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
              gap: 16px;
            }

            .card {
              background: var(--card);
              border-radius: 14px;
              box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
              padding: 18px;
            }

            h1, h2 { margin: 0 0 12px 0; }
            .topic { color: var(--muted); margin: 0 0 6px 0; }
            .meta { color: var(--muted); margin-top: 0; font-size: 0.9rem; }

            label { display: block; margin: 10px 0 6px; font-weight: 600; }
            input {
              width: 100%;
              padding: 10px;
              border: 1px solid #cbd5e1;
              border-radius: 8px;
              font-size: 14px;
            }

            button {
              margin-top: 12px;
              background: var(--brand);
              color: white;
              border: 0;
              border-radius: 8px;
              padding: 10px 12px;
              cursor: pointer;
              font-weight: 700;
            }

            pre {
              margin-top: 10px;
              background: #0b1220;
              color: #e2e8f0;
              border-radius: 8px;
              padding: 10px;
              min-height: 110px;
              overflow: auto;
            }
            """
        ),
    )

    write(
        app_root / "frontend" / "app.js",
        dedent(
            """\
            async function fetchJson(url, options) {
              const response = await fetch(url, options);
              if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
              }
              return response.json();
            }

            function parseValues(raw) {
              return raw
                .split(",")
                .map((v) => Number(v.trim()))
                .filter((v) => Number.isFinite(v));
            }

            document.getElementById("meta-btn").addEventListener("click", async () => {
              const box = document.getElementById("meta-box");
              box.textContent = "loading...";
              try {
                const data = await fetchJson("/v1/project/meta");
                box.textContent = JSON.stringify(data, null, 2);
              } catch (error) {
                box.textContent = String(error);
              }
            });

            document.getElementById("run-btn").addEventListener("click", async () => {
              const valuesRaw = document.getElementById("values").value;
              const note = document.getElementById("note").value || "frontend-run";
              const payload = {
                values: parseValues(valuesRaw),
                note,
              };

              const box = document.getElementById("run-box");
              box.textContent = "running...";
              try {
                const data = await fetchJson("/v1/project/run", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(payload),
                });
                box.textContent = JSON.stringify(data, null, 2);
              } catch (error) {
                box.textContent = String(error);
              }
            });
            """
        ),
    )

    write(
        app_root / "README.md",
        dedent(
            f"""\
            # {project_id} App ({prj_name})

            - Track: `{track_code}`
            - Topic: `{topic}`
            - Curriculum Link: `{md_file}`

            ## Modules
            - `backend/app/core.py`: pure Python scenario logic
            - `backend/app/main.py`: FastAPI service
            - `frontend/`: FE static module

            ## Local Run
            ```bash
            cd {app_root.relative_to(ROOT).as_posix()}
            python -m venv .venv
            source .venv/bin/activate
            pip install -r requirements.txt
            python -m uvicorn backend.app.main:app --reload --port 8080
            ```

            ## Test
            ```bash
            python -m unittest discover -s backend/tests -p 'test_*.py'
            ```

            ## Docker
            ```bash
            docker compose up -d --build
            # health
            curl -sS http://127.0.0.1:{host_port}/health
            ```
            """
        ),
    )


def build_master_readme(rows: list[dict[str, str]]) -> str:
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        prj_name = project_name_from_md_file(row.get("md_file", ""))
        groups.setdefault(prj_name, []).append(row)

    lines = [
        "# Project Apps (Merged)",
        "",
        "`project/` 폴더 안에 커리큘럼 자료와 실행/테스트용 앱(FastAPI + FE + Docker)을 통합 구성합니다.",
        "",
        "구성: 각 프로젝트별 `Python core + FastAPI + FE + Docker + tests`",
        "",
        "## Groups",
    ]

    for prj_name in sorted(groups.keys()):
        lines.append(f"- `{prj_name}`")
        for row in sorted(groups[prj_name], key=lambda r: r["class"]):
            project_id = row["class"]
            project_num = int(project_id.replace("project", ""))
            port = 9100 + project_num
            topic = topic_from_module(row.get("module", ""))
            lines.append(f"  - `{project_id}`: `{topic}` (docker port `{port}`)")

    lines.extend(
        [
            "",
            "## Quick Start (example)",
            "```bash",
            "cd VoiceModelBuilder",
            "python -m venv .venv",
            "source .venv/bin/activate",
            "pip install -r requirements.txt",
            "python -m uvicorn backend.app.main:app --reload --port 8080",
            "```",
            "",
            "## Docker",
            "```bash",
            "cd VoiceModelBuilder",
            "docker compose up -d --build",
            "curl -sS http://127.0.0.1:9101/health",
            "```",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    rows = load_project_rows()
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []
    for row in rows:
        scaffold_project(row)
        project_id = row["class"].strip()
        project_num = int(project_id.replace("project", ""))
        app_rel = class_dir_from_row(row).relative_to(ROOT).as_posix()
        manifest.append(
            {
                "project_id": project_id,
                "track": row.get("subject_code", "").strip(),
                "topic": topic_from_module(row.get("module", "")),
                "group": project_name_from_md_file(row.get("md_file", "")),
                "docker_port": 9100 + project_num,
                "app_path": app_rel,
            }
        )

    write(PROJECT_ROOT / "README.md", build_master_readme(rows))
    write(PROJECT_ROOT / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    print(f"Scaffolded apps: {len(rows)}")
    print(f"Root: {PROJECT_ROOT}")


if __name__ == "__main__":
    main()
