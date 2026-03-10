# project002 · 거대 언어 모델을 활용한 PERSONA AI 답변 기능 구현하기

독립 실행형 PERSONA 답변 프로젝트입니다.

## 기능
- Persona 등록/수정
- Persona별 질문 응답 생성
- OpenAI 키가 있으면 LLM 응답, 없으면 로컬 규칙 응답

## 실행
```bash
cd project/Prj_PersonaVoiceAI/project002
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8080
```

## Docker
```bash
docker compose up -d --build
curl -sS http://127.0.0.1:9102/health
```
