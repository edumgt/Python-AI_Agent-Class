# Project Apps (3 Independent Projects)

`project/Prj_PersonaVoiceAI`는 아래 3개만 독립 실행 프로젝트로 구성됩니다.

## Projects
1. `project001`  
   - 주제: `나만의 음성 모델 만들기`
   - 경로: `project/Prj_PersonaVoiceAI/project001`
   - 포트: `9101`

2. `project002`  
   - 주제: `거대 언어 모델을 활용한 PERSONA AI 답변 기능 구현하기`
   - 경로: `project/Prj_PersonaVoiceAI/project002`
   - 포트: `9102`

3. `project003`  
   - 주제: `사전 데이터 기반 PERSO AI의 답변 커스텀하기`
   - 경로: `project/Prj_PersonaVoiceAI/project003`
   - 포트: `9103`

## 공통 실행
```bash
cd project/Prj_PersonaVoiceAI/project001  # 또는 project002, project003
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8080
```

## Docker
```bash
cd project/Prj_PersonaVoiceAI/project001  # 또는 project002, project003
docker compose up -d --build
curl -sS http://127.0.0.1:9101/health
```
