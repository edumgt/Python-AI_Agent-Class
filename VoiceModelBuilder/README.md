# VoiceModelBuilder · 나만의 음성 모델 만들기

독립 실행형 음성 모델 실습 프로젝트입니다.

## 기능
- 음성 프로필 생성
- 학습 품질 시뮬레이션
- SSML 기반 합성 프리뷰 생성

## 실행
```bash
cd VoiceModelBuilder
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8080
```

## Docker
```bash
docker compose up -d --build
curl -sS http://127.0.0.1:9101/health
```
