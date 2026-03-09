# project014 App (Prj_LLMOpsRAGQuality)

- Track: `프로젝트-3`
- Topic: `LLMOps/RAG 서비스 품질관리 · 단계 4/5 실전 검증`
- Curriculum Link: `project/Prj_LLMOpsRAGQuality/project014/project014.md`

## Modules
- `backend/app/core.py`: pure Python scenario logic
- `backend/app/main.py`: FastAPI service
- `frontend/`: FE static module

## Local Run
```bash
cd projectApps/Prj_LLMOpsRAGQuality/project014
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
curl -sS http://127.0.0.1:9114/health
```
