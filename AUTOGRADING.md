# Auto Grading (테스트 기반 업그레이드)

이 패키지는 **출력 문자열 비교**가 아니라, 아래 방식으로 채점합니다.

- **함수 단위 검증**: 학생이 구현해야 하는 핵심 함수(`even_squares`, `make_plot`, `make_data`, `build_df`, `build_prompt` 등)를 직접 호출해 결과를 검사
- **결과 파일 검증**: `outputs/result.json`, `outputs/plot.png`, `outputs/data.csv` 같은 산출물이 실제로 생성되었는지와 형식을 확인
- **구조 검증**: DataFrame 컬럼, PromptTemplate 변수, 회귀 MSE 범위처럼 과제 목적에 맞는 구조까지 점검
- **정답 코드 존재 검증**: `classXXX_solution.py`가 import 가능한지도 함께 확인

> 주의: 학생용 과제 파일(`*_assignment_*.py`)은 **TODO를 구현한 뒤** 채점해야 합니다.

## 지원되는 과제 패턴

1. **Python 기초**
   - `even_squares`, `divide`, `save_result`
   - JSON 저장 내용까지 확인

2. **시각화**
   - `make_plot`
   - PNG 파일 실제 생성 여부 + PNG 시그니처 검증

3. **머신러닝 회귀**
   - `make_data`, `train_and_eval`
   - 데이터 shape + MSE 범위 검증

4. **데이터프레임 I/O**
   - `build_df`, `save_and_load`
   - 컬럼/합계/평균 + CSV 저장/재로딩 shape 검증

5. **프롬프트 엔지니어링**
   - `build_prompt`
   - `role`, `question` 변수와 렌더링 결과 검증

## 사용법

### 단일 차시

```bash
python grade_class.py class001 --tier basic
python grade_class.py class120 --tier advanced
python grade_class.py class500 --tier challenge
```

### 전체 차시

```bash
python grade_all.py --tier basic
python grade_all.py --tier advanced --start class101 --end class200
```

### Windows PowerShell

```powershell
python .\grade_class.py class041 --tier basic
python .\grade_all.py --tier challenge
```

## 출력 예시

- `PROFILE`: 과제 유형 자동 감지 결과
- `PASS/FAIL`: 체크 항목별 결과
- `RESULT`: 최종 합격/불합격

## 파일 구성

- `grader_core.py` : 실제 테스트 로직
- `grade_class.py` : 단일 차시 채점기
- `grade_all.py` : 일괄 채점기

필요하면 다음 단계로도 확장할 수 있습니다.
- 과제별 **루브릭 점수화(100점 만점)**
- 과목별 **개별 테스트 시나리오**
- 제출물 폴더를 따로 받아 채점하는 **제출 전용 채점기**
