# Project Index (Top-Level Apps)

프로젝트 앱은 `Agent/`와 동일하게 저장소 루트 상위로 이동되었습니다.

## Projects
1. `VoiceModelBuilder`
   - 주제: `나만의 음성 모델 만들기`
   - 경로: `VoiceModelBuilder`
   - 포트: `9101`

2. `PersonaLLMResponder`
   - 주제: `거대 언어 모델을 활용한 PERSONA AI 답변 기능 구현하기`
   - 경로: `PersonaLLMResponder`
   - 포트: `9102`

3. `PersonaKnowledgeCustomizer`
   - 주제: `사전 데이터 기반 PERSO AI의 답변 커스텀하기`
   - 경로: `PersonaKnowledgeCustomizer`
   - 포트: `9103`

## 공통 실행
```bash
cd VoiceModelBuilder  # 또는 PersonaLLMResponder, PersonaKnowledgeCustomizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8080
```

## Docker
```bash
cd VoiceModelBuilder  # 또는 PersonaLLMResponder, PersonaKnowledgeCustomizer
docker compose up -d --build
curl -sS http://127.0.0.1:9101/health
```
