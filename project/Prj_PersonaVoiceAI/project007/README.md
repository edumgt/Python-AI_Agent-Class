# project007 App (Prj_PersonaVoiceAI)

- Track: `프로젝트-2`
- Topic: `PERSONA 코칭 대화 파이프라인(STT↔LLM↔TTS) · 단계 2/5 기초 구현`
- Curriculum Link: `project/Prj_PersonaVoiceAI/project007/project007.md`

## Modules
- `backend/app/core.py`: pure Python scenario logic
- `backend/app/main.py`: FastAPI service
- `frontend/`: FE static module

## Local Run
```bash
cd project/Prj_PersonaVoiceAI/project007
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
curl -sS http://127.0.0.1:9107/health
```
