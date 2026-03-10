# Project Apps (Merged)

`project/` 폴더 안에 커리큘럼 자료와 실행/테스트용 앱(FastAPI + FE + Docker)을 통합 구성합니다.

구성: 각 프로젝트별 `Python core + FastAPI + FE + Docker + tests`

## Groups
- `Prj_PersonaVoiceAI`
  - `project001`: `개인 맞춤 코칭 음성봇 PERSONA AI 만들기 · 단계 1/5 입문 이해` (docker port `9101`)
  - `project002`: `개인 맞춤 코칭 음성봇 PERSONA AI 만들기 · 단계 2/5 기초 구현` (docker port `9102`)
  - `project003`: `개인 맞춤 코칭 음성봇 PERSONA AI 만들기 · 단계 3/5 응용 확장` (docker port `9103`)
  - `project004`: `개인 맞춤 코칭 음성봇 PERSONA AI 만들기 · 단계 4/5 실전 검증` (docker port `9104`)
  - `project005`: `개인 맞춤 코칭 음성봇 PERSONA AI 만들기 · 단계 5/5 운영 최적화` (docker port `9105`)
  - `project006`: `PERSONA 코칭 대화 파이프라인(STT↔LLM↔TTS) · 단계 1/5 입문 이해` (docker port `9106`)
  - `project007`: `PERSONA 코칭 대화 파이프라인(STT↔LLM↔TTS) · 단계 2/5 기초 구현` (docker port `9107`)
  - `project008`: `PERSONA 코칭 대화 파이프라인(STT↔LLM↔TTS) · 단계 3/5 응용 확장` (docker port `9108`)
  - `project009`: `PERSONA 코칭 대화 파이프라인(STT↔LLM↔TTS) · 단계 4/5 실전 검증` (docker port `9109`)
  - `project010`: `PERSONA 코칭 대화 파이프라인(STT↔LLM↔TTS) · 단계 5/5 운영 최적화` (docker port `9110`)
  - `project011`: `사전 데이터 기반 PERSONA AI 구축 · 단계 1/5 입문 이해` (docker port `9111`)
  - `project012`: `사전 데이터 기반 PERSONA AI 구축 · 단계 2/5 기초 구현` (docker port `9112`)
  - `project013`: `사전 데이터 기반 PERSONA AI 구축 · 단계 3/5 응용 확장` (docker port `9113`)
  - `project014`: `사전 데이터 기반 PERSONA AI 구축 · 단계 4/5 실전 검증` (docker port `9114`)
  - `project015`: `사전 데이터 기반 PERSONA AI 구축 · 단계 5/5 운영 최적화` (docker port `9115`)
  - `project016`: `PERSONA AI 지속학습과 품질 운영 · 단계 1/5 입문 이해` (docker port `9116`)
  - `project017`: `PERSONA AI 지속학습과 품질 운영 · 단계 2/5 기초 구현` (docker port `9117`)
  - `project018`: `PERSONA AI 지속학습과 품질 운영 · 단계 3/5 응용 확장` (docker port `9118`)
  - `project019`: `PERSONA AI 지속학습과 품질 운영 · 단계 4/5 실전 검증` (docker port `9119`)
  - `project020`: `PERSONA AI 지속학습과 품질 운영 · 단계 5/5 운영 최적화` (docker port `9120`)

## Quick Start (example)
```bash
cd project/Prj_PersonaVoiceAI/project001
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8080
```

## Docker
```bash
cd project/Prj_PersonaVoiceAI/project001
docker compose up -d --build
curl -sS http://127.0.0.1:9101/health
```
