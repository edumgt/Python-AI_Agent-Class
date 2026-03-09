# project010 App (Prj_MLOpsPipeline)

- Track: `프로젝트-2`
- Topic: `MLOps 파이프라인과 모델 레지스트리 · 단계 5/5 운영 최적화`
- Curriculum Link: `project/Prj_MLOpsPipeline/project010/project010.md`

## Modules
- `backend/app/core.py`: pure Python scenario logic
- `backend/app/main.py`: FastAPI service
- `frontend/`: FE static module

## Local Run
```bash
cd projectApps/Prj_MLOpsPipeline/project010
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
curl -sS http://127.0.0.1:9110/health
```
