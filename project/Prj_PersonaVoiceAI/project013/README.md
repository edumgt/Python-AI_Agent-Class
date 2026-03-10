# project013 App (Prj_PersonaVoiceAI)

- Track: `프로젝트-3`
- Topic: `사전 데이터 기반 PERSONA AI 구축 · 단계 3/5 응용 확장`
- Curriculum Link: `project/Prj_PersonaVoiceAI/project013/project013.md`

## Modules
- `backend/app/core.py`: pure Python scenario logic
- `backend/app/main.py`: FastAPI service
- `frontend/`: FE static module

## Local Run
```bash
cd project/Prj_PersonaVoiceAI/project013
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
curl -sS http://127.0.0.1:9113/health
```
