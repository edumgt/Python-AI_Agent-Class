# project004 App (Prj_DevOpsKickoff)

- Track: `프로젝트-1`
- Topic: `DevOps 프로젝트 착수와 요구사항 정의 · 단계 4/5 실전 검증`
- Curriculum Link: `project/Prj_DevOpsKickoff/project004/project004.md`

## Modules
- `backend/app/core.py`: pure Python scenario logic
- `backend/app/main.py`: FastAPI service
- `frontend/`: FE static module

## Local Run
```bash
cd projectApps/Prj_DevOpsKickoff/project004
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
curl -sS http://127.0.0.1:9104/health
```
