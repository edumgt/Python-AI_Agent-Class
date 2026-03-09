<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class064 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **Python 전처리 및 시각화**
- 학습 주제: **그룹화와 집계 · 단계 4/4 운영 최적화 [class064]**
- 학습 주제 진행: **그룹화와 집계 · 단계 4/4 운영 최적화 [class064] (총 4시간 중 4시간차)**
- 세부 시퀀스: **24/40**
- 일정: **Day 08 / 8교시**
- 최종 목표: **Agent 폴더의 실제 시스템 구성요소를 구현·연동·운영할 수 있는 개발자 역량 확보**
- 난이도: **기초응용**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `Python 전처리 및 시각화`
- 문법 포인트: 명사구를 연결어 '및'으로 병렬 연결한 구조입니다. 동등한 학습 범위를 함께 제시합니다.
- 기술 포인트: 데이터 전처리와 시각화를 통해 분석 가능한 정보로 바꾸는 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `Python` | 고유명사(언어명) | Python (한자 없음) | Python | 데이터 처리와 AI 실습에 널리 쓰이는 범용 프로그래밍 언어입니다. |
| `전처리` | 명사 | 전처리 (前處理) | preprocessing | 원시 데이터를 모델이 다루기 쉬운 형태로 정리하는 단계입니다. |
| `시각화` | 명사 | 시각화 (視覺化) | visualization | 숫자 데이터를 그래프와 차트로 표현해 패턴을 해석하는 과정입니다. |

#### 학습주제 표현 분석: `그룹화와 집계 · 단계 4/4 운영 최적화 [class064]`
- 문법 포인트: 명사와 명사를 대등하게 묶는 병렬 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `그룹화와 집계 · 단계 4/4 운영 최적화 [class064]`를 중심으로 같은 주제 내에서 단계적으로 고도화된 구현을 수행합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `그룹화` | 명사 | 그룹화 (그룹化) | grouping | 공통 키 기준으로 데이터를 묶어 집계 가능한 형태로 만듭니다. |
| `집계` | 명사 | 집계 (集計) | aggregation | 합계, 평균, 개수 등 통계량을 계산하는 단계입니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class063 / 그룹화와 집계 · 단계 3/4 실전 검증 [class063]** (Day 08 / 7교시)
- 복습 연결: 이전에 배운 **그룹화와 집계 · 단계 3/4 실전 검증 [class063]** 를 떠올리며, 오늘 **그룹화와 집계 · 기능 통합 예외 흐름 정의 (차시 24) [class064]** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: 그룹화와 집계를 단계 4/4(운영 최적화) 수준으로 고도화해 구현하는 차시입니다.
- 왜 배우나요?: 동일 주제를 반복하더라도 단계별 난이도를 높여 실무 수준의 문제 해결력을 만들기 위해서입니다.

### 핵심 개념 3가지
1. `그룹화와 집계`의 핵심 입력/출력 구조를 단계 4/4 기준으로 명확히 정의합니다.
2. `운영 최적화` 수준에서 필요한 구현 패턴(검증, 예외, 로깅, 성능)을 코드에 반영합니다.
3. 이전 단계 결과를 재사용해 다음 단계로 확장 가능한 구조로 리팩터링합니다.

### 비유로 이해하기
- 기초 공정에서 시작해 품질검사와 운영튜닝까지 단계적으로 완성도를 올리는 제조 라인과 같습니다.
## 4) 실습 환경 만들기 (항상 먼저)
아래 명령은 **처음 한 번** 준비해 두면 이후 학습이 쉬워집니다.

### Windows PowerShell
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Linux/macOS (bash)
```bash
cd /path/to/Python-AI_Agent-Class
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5) 오늘의 예제 코드
- 예제 파일: `class064_example1.py`
- 실행 명령:
```bash
python dataVizPrep/class064/class064_example1.py
```


<!-- AUTO-GENERATED: OS_COMMANDS START -->
## 5-1) 운영체제별 실행 명령 예시
### PowerShell (Windows)
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python .\dataVizPrep\class064\class064.py
python .\dataVizPrep\class064\class064_example1.py
python .\dataVizPrep\class064\class064_assignment.py
start .\dataVizPrep\class064\class064_quiz.html
```

### WSL Ubuntu (bash)
```bash
cd /mnt/c/DevOps/Python-AI_Agent-Class
python3 dataVizPrep/class064/class064.py
python3 dataVizPrep/class064/class064_example1.py
python3 dataVizPrep/class064/class064_assignment.py
explorer.exe "$(wslpath -w 'dataVizPrep/class064/class064_quiz.html')"
```

### run_class/run_day 스크립트 연동 (WSL bash)
```bash
./run_class.sh class064
./run_day.sh 8 launcher
```
<!-- AUTO-GENERATED: OS_COMMANDS END -->

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python dataVizPrep/class064/class064_example1.py`)
- 주요 문법: `함수`, `리스트/딕셔너리`, `집계 로직`, `출력(print)`
- 학습 포커스: `그룹화와 집계 · 단계 4/4 운영 최적화 [class064]`

### 실습 example1.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class064 (24/40, 기초응용)"]
N2["학습 주제 파악: 그룹화와 집계 · 단계 4/4 운영 최적화 [class064]"]
N3["1단계: 원본 데이터를 로딩하고 구조를 확인한다"]
N4["2단계: 결측치/이상치를 전처리한다"]
N5["3단계: 집계·변환으로 분석용 데이터를 만든다"]
N6["4단계: 요약 결과를 표/리포트로 검증한다"]
N7["예제 실행: python dataVizPrep/class064/class064_example1.py"]
N8["다음 준비: 그룹화와 집계 · 단계 4/4 운영 최적화 [class064] 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class064 flow](class064_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 입력이 무엇인지 먼저 찾기
2. 처리 규칙(함수/조건/반복) 확인하기
3. 출력 결과가 목표와 맞는지 점검하기

## 6) 퀴즈로 복습하기 (5문항)
- 퀴즈 파일: `class064_quiz.html`
- 브라우저에서 열기:
```bash
dataVizPrep/class064/class064_quiz.html
```
- 버튼 설명:
1. `채점하기`: 현재 선택한 답으로 점수를 계산해요.
2. `다시풀기`: 선택을 모두 지우고 처음부터 다시 풀어요.

## 7) 혼자 실습 순서 (초등학생 버전)
1. 코드를 한 번 그대로 실행해요.
2. 숫자/문장 값을 1개 바꿔요.
3. 결과가 왜 바뀌었는지 한 줄로 적어요.
4. 함수를 1개 더 만들어 작은 기능을 추가해요.

### 실습 미션
1. `그룹화와 집계` 단계 4/4 목표 기능을 코드로 구현하고 실행 로그를 남기세요.
2. `운영 최적화` 관점에서 실패 케이스 1개 이상을 재현하고 대응 코드를 추가하세요.
3. 이전 단계 코드와 비교해 변경점(입력/처리/출력)을 3줄로 정리하세요.

## 8) 스스로 점검 체크리스트
- [ ] 데이터 항목 이름을 정확히 이해했다.
- [ ] 정리 전/정리 후 차이를 설명할 수 있다.
- [ ] 평균/최댓값/최솟값 중 1개 이상을 계산했다.

## 9) 막히면 이렇게 해결해요
1. 에러 메시지 마지막 줄을 먼저 읽어요.
2. 함수 이름과 괄호 짝을 확인해요.
3. `print()`를 넣어 중간 값을 확인해요.
4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

## 10) 학습 후 다음에 배울 내용
- 다음 차시: **class065 / 데이터 병합과 변환 · 단계 1/4 입문 이해 [class065]** (Day 09 / 1교시)
- 미리보기: 다음 차시 전에 **그룹화와 집계 · 단계 4/4 운영 최적화 [class064]** 핵심 코드 1개를 다시 실행해 두면 데이터 병합과 변환 · 단계 1/4 입문 이해 [class065] 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 더 큰 데이터에서도 같은 정리 원칙을 적용해 볼 거예요.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
