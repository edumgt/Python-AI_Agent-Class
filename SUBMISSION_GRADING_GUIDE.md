# 제출형 채점 가이드

기본 채점기는 각 `classXXX` 폴더 안의 학생용 과제 파일을 직접 검사합니다.
운영 시 아래 순서로 사용하면 편합니다.

1. 학생이 `classXXX_assignment_basic.py` 등을 완성
2. 강사가 루트에서 `python grade_class.py classXXX --tier basic` 실행
3. PASS/FAIL 항목을 보고 즉시 피드백

## 추천 운영 방식

- **수업 중간**: `basic` 난이도만 빠르게 점검
- **수업 종료 전**: `advanced` 또는 `challenge` 재채점
- **주간 점검**: `python grade_all.py --tier basic --start class001 --end class040`

## 실패 원인 예시

- `NotImplementedError` : TODO 미구현
- `file not found` : 결과 파일 저장 누락
- `missing columns` : DataFrame 컬럼 미완성
- `MSE too large` : 모델 학습 로직 이상
- `unresolved template markers remain` : 프롬프트 변수 치환 누락
