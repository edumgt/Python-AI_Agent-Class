# Project Apps

`projectApps/`는 커리큘럼용 `project/` 폴더와 분리된 실행/테스트용 애플리케이션 묶음입니다.

구성: 각 프로젝트별 `Python core + FastAPI + FE + Docker + tests`

## Groups
- `Prj_AIOpsObservability`
  - `project016`: `AIOps 관측성·이상탐지·자동복구 · 단계 1/5 입문 이해` (docker port `9116`)
  - `project017`: `AIOps 관측성·이상탐지·자동복구 · 단계 2/5 기초 구현` (docker port `9117`)
  - `project018`: `AIOps 관측성·이상탐지·자동복구 · 단계 3/5 응용 확장` (docker port `9118`)
  - `project019`: `AIOps 관측성·이상탐지·자동복구 · 단계 4/5 실전 검증` (docker port `9119`)
  - `project020`: `AIOps 관측성·이상탐지·자동복구 · 단계 5/5 운영 최적화` (docker port `9120`)
- `Prj_DevOpsKickoff`
  - `project001`: `DevOps 프로젝트 착수와 요구사항 정의 · 단계 1/5 입문 이해` (docker port `9101`)
  - `project002`: `DevOps 프로젝트 착수와 요구사항 정의 · 단계 2/5 기초 구현` (docker port `9102`)
  - `project003`: `DevOps 프로젝트 착수와 요구사항 정의 · 단계 3/5 응용 확장` (docker port `9103`)
  - `project004`: `DevOps 프로젝트 착수와 요구사항 정의 · 단계 4/5 실전 검증` (docker port `9104`)
  - `project005`: `DevOps 프로젝트 착수와 요구사항 정의 · 단계 5/5 운영 최적화` (docker port `9105`)
- `Prj_LLMOpsRAGQuality`
  - `project011`: `LLMOps/RAG 서비스 품질관리 · 단계 1/5 입문 이해` (docker port `9111`)
  - `project012`: `LLMOps/RAG 서비스 품질관리 · 단계 2/5 기초 구현` (docker port `9112`)
  - `project013`: `LLMOps/RAG 서비스 품질관리 · 단계 3/5 응용 확장` (docker port `9113`)
  - `project014`: `LLMOps/RAG 서비스 품질관리 · 단계 4/5 실전 검증` (docker port `9114`)
  - `project015`: `LLMOps/RAG 서비스 품질관리 · 단계 5/5 운영 최적화` (docker port `9115`)
- `Prj_MLOpsPipeline`
  - `project006`: `MLOps 파이프라인과 모델 레지스트리 · 단계 1/5 입문 이해` (docker port `9106`)
  - `project007`: `MLOps 파이프라인과 모델 레지스트리 · 단계 2/5 기초 구현` (docker port `9107`)
  - `project008`: `MLOps 파이프라인과 모델 레지스트리 · 단계 3/5 응용 확장` (docker port `9108`)
  - `project009`: `MLOps 파이프라인과 모델 레지스트리 · 단계 4/5 실전 검증` (docker port `9109`)
  - `project010`: `MLOps 파이프라인과 모델 레지스트리 · 단계 5/5 운영 최적화` (docker port `9110`)

## Quick Start (example)
```bash
cd projectApps/Prj_DevOpsKickoff/project001
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8080
```

## Docker
```bash
cd projectApps/Prj_DevOpsKickoff/project001
docker compose up -d --build
curl -sS http://127.0.0.1:9101/health
```
