<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# Python , AI Agent Curriculum Classes 001-500

첨부 커리큘럼의 **정규교과 500시간**만 기준으로 세분화한 교육 저장소입니다.
프로젝트 과정은 제외되어 있으며, `class001`부터 `class500`까지 각 차시별 학습 자료가 포함됩니다.

## 구성 범위
- 대상: 정규교과 500개 차시
- 제외: 프로젝트 과정
- 운영 방식: **설명 10분 + 실습 30분 + 정리 10분**
- 일 운영 기준: **하루 8시간**

## 저장소 구조
- `class001/` ~ `class500/`
  - `classXXX.md` : 차시 개요
  - `classXXX.py` : 기본 실행 런처
  - `classXXX_solution.py` : 정답 코드
  - `classXXX_assignment.py` : 과제 디스패처
  - `classXXX_assignment_basic.py` : 기본 과제
  - `classXXX_assignment_advanced.py` : 심화 과제
  - `classXXX_assignment_challenge.py` : 챌린지 과제
  - `instructor_notes.md` : 강사용 해설서
- `curriculum_index.csv` : 전체 차시 인덱스
- `INSTRUCTOR_GUIDE.md` : 강의 운영 가이드
- `AUTOGRADING.md` : 자동채점 안내
- `SUBMISSION_GRADING_GUIDE.md` : 제출/채점 안내

## 빠른 시작
```bash
python class001/class001.py
```

기본 과제 실행:
```bash
python class001/class001_assignment.py
```

심화 과제 실행:
```bash
CLASS_TIER=advanced python class001/class001_assignment.py
```

챌린지 과제 실행:
```bash
CLASS_TIER=challenge python class001/class001_assignment.py
```

## 자동채점
개별 차시 채점:
```bash
python grade_class.py class001 --tier basic
```

전체 차시 채점:
```bash
python grade_all.py --tier basic
```

## GitHub Actions
푸시/PR 시 자동으로:
- Python 문법 체크
- 기본 자동채점 샘플 실행
- 저장소 구조 확인

워크플로우 파일:
- `.github/workflows/autograde.yml`

## 권장 브랜치 운영
- `main` : 배포/기준 브랜치
- `develop` : 통합 개발 브랜치
- `feature/class-xxx-*` : 차시별 수정

## 라이선스
이 저장소에는 기본적으로 `MIT License`가 포함되어 있습니다.
상용/사내 배포 전에는 교육기관 정책에 맞게 라이선스를 검토하세요.
