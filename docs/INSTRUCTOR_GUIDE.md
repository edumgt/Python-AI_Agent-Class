<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
## 자동채점 업그레이드 안내
- 현재 패키지는 **함수 단위 테스트 + 결과 파일 검증** 기반 자동채점을 포함합니다.
- 루트의 `AUTOGRADING.md`, `SUBMISSION_GRADING_GUIDE.md`를 함께 참고하세요.

# 강사용 운영 가이드 (전체)

## 폴더 구조
- 과목 폴더(예: `pyBasics`, `dataVizPrep`, `mlDeepDive`) 아래 `classXXX/`가 위치
- classXXX/
  - classXXX.md : 차시 개요(설명/실습/정리)
  - classXXX.py : 기본 실행 런처(과제 실행)
  - classXXX_assignment.py : 학생용 과제(빈칸/TODO)
  - classXXX_solution.py : 강사용 정답 예시
  - instructor_notes.md : 강사용 해설서(10/30/10 진행, 실수 포인트, 루브릭)

## 수업 운영 팁 (하루 8시간)
- 1일 8교시 기준으로 class001~class008이 Day01에 해당
- 매 교시마다:
  - 설명 10분: 목표/산출물 먼저 보여주기(파일/출력)
  - 실습 30분: TODO 구현 + 중간 체크포인트(10/20/30분)
  - 정리 10분: 리팩토링 1개 + Q&A

## 실행 방법
- (권장) 가상환경:
  - python -m venv .venv
  - Windows: .venv\Scripts\activate
  - Linux/macOS: source .venv/bin/activate
  - pip install -r requirements.txt
  - 설명 포인트: `.venv`는 프로젝트 전용 Python 폴더(인터프리터+패키지)이며, 전역 환경과 분리해 버전 충돌을 줄이고 실습 재현성을 높임

- 개별 차시:
  - python pyBasics/class001/class001.py
  - 또는 python pyBasics/class001/class001_assignment.py

## 채점/피드백
- 기능(70) / 가독성(20) / 확장(10) 루브릭을 instructor_notes.md에 기본 제공
- 학생 제출은 assignment.py만 받는 것을 권장

## 자동채점

- 자동채점 안내: `AUTOGRADING.md`
- 단일 채점: `python grade_class.py class001 --tier basic`
- 전체 채점: `python grade_all.py --tier basic`
