# project003 · 사전 데이터 기반 PERSO AI의 답변 커스텀하기

독립 실행형 지식 커스텀 답변 프로젝트입니다.

## 기능
- 지식 데이터 업서트/조회
- 기본 지식 부트스트랩
- 질문 기반 검색 후 PERSO 스타일 답변 생성

## 실행
```bash
cd project/Prj_PersonaVoiceAI/project003
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8080
```

## Docker
```bash
docker compose up -d --build
curl -sS http://127.0.0.1:9103/health
```
