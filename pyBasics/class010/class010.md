<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class010 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **Python 프로그래밍**
- 학습 주제: **연산자와 조건문 · 단계 2/4 기초 구현 [class010]**
- 학습 주제 진행: **연산자와 조건문 · 단계 2/4 기초 구현 [class010] (총 4시간 중 2시간차)**
- 세부 시퀀스: **10/40**
- 일정: **Day 02 / 2교시**
- 최종 목표: **Agent 폴더의 실제 시스템 구성요소를 구현·연동·운영할 수 있는 개발자 역량 확보**
- 난이도: **기초응용**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `Python 프로그래밍`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 코드 문법을 통해 문제를 절차적으로 해결하는 역량을 기르는 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `Python` | 고유명사(언어명) | Python (한자 없음) | Python | 데이터 처리와 AI 실습에 널리 쓰이는 범용 프로그래밍 언어입니다. |
| `프로그래밍` | 명사 | 프로그래밍 (한자 없음) | programming | 문제를 알고리즘으로 분해해 코드로 구현하는 활동입니다. |

#### 학습주제 표현 분석: `연산자와 조건문 · 단계 2/4 기초 구현 [class010]`
- 문법 포인트: 명사와 명사를 대등하게 묶는 병렬 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `연산자와 조건문 · 단계 2/4 기초 구현 [class010]`를 중심으로 같은 주제 내에서 단계적으로 고도화된 구현을 수행합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `연산자` | 명사 | 연산자 (演算子) | operator | 피연산자에 연산 규칙을 적용하는 기호/키워드입니다. |
| `조건문` | 명사 | 조건문 (條件文) | conditional statement | 조건 평가 결과에 따라 실행 분기를 선택하는 문법입니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class009 / 연산자와 조건문 · 단계 1/4 입문 이해 [class009]** (Day 02 / 1교시)
- 복습 연결: 이전에 배운 **연산자와 조건문 · 단계 1/4 입문 이해 [class009]** 를 떠올리며, 오늘 **연산자와 조건문 · 핵심 구현 로그 포맷 설계 (차시 10) [class010]** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: 연산자와 조건문를 단계 2/4(기초 구현) 수준으로 고도화해 구현하는 차시입니다.
- 왜 배우나요?: 동일 주제를 반복하더라도 단계별 난이도를 높여 실무 수준의 문제 해결력을 만들기 위해서입니다.

### 핵심 개념 3가지
1. `연산자와 조건문`의 핵심 입력/출력 구조를 단계 2/4 기준으로 명확히 정의합니다.
2. `기초 구현` 수준에서 필요한 구현 패턴(검증, 예외, 로깅, 성능)을 코드에 반영합니다.
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
- 예제 파일: `class010_example1.py`
- 실행 명령:
```bash
python pyBasics/class010/class010_example1.py
```


<!-- AUTO-GENERATED: OS_COMMANDS START -->
## 5-1) 운영체제별 실행 명령 예시
### PowerShell (Windows)
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python .\pyBasics\class010\class010.py
python .\pyBasics\class010\class010_example1.py
python .\pyBasics\class010\class010_assignment.py
start .\pyBasics\class010\class010_quiz.html
```

### WSL Ubuntu (bash)
```bash
cd /mnt/c/DevOps/Python-AI_Agent-Class
python3 pyBasics/class010/class010.py
python3 pyBasics/class010/class010_example1.py
python3 pyBasics/class010/class010_assignment.py
explorer.exe "$(wslpath -w 'pyBasics/class010/class010_quiz.html')"
```

### run_class/run_day 스크립트 연동 (WSL bash)
```bash
./run_class.sh class010
./run_day.sh 2 launcher
```
<!-- AUTO-GENERATED: OS_COMMANDS END -->

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python pyBasics/class010/class010_example1.py`)
- 주요 문법: `산술/비교/논리 연산자`, `if / elif / else`, `단락 평가(and, or)`, `멤버십(in, not in)`
- 학습 포커스: `연산자와 조건문 · 단계 2/4 기초 구현 [class010]`

### 실습 example1.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class010 (10/40, 기초응용)"]
N2["학습 주제 파악: 연산자와 조건문 · 단계 2/4 기초 구현 [class010]"]
N3["1단계: 요구사항을 불리언 조건식으로 변환한다"]
N4["2단계: 연산자 우선순위를 정리해 조건식을 확정한다"]
N5["3단계: if/elif/else로 분기 경로를 구현한다"]
N6["4단계: 경계값 테스트로 분기 누락 여부를 검증한다"]
N7["예제 실행: python pyBasics/class010/class010_example1.py"]
N8["다음 준비: 연산자와 조건문 · 단계 2/4 기초 구현 [class010] 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class010 flow](class010_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 조건식이 최종적으로 `True/False`로 귀결되는지 확인하기
2. 분기별 출력이 명확하게 구분되는지 확인하기
3. 단락 평가를 활용해 불필요한 계산과 오류를 줄였는지 점검하기

## 6) 퀴즈로 복습하기 (5문항)
- 퀴즈 파일: `class010_quiz.html`
- 브라우저에서 열기:
```bash
pyBasics/class010/class010_quiz.html
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
1. `연산자와 조건문` 단계 2/4 목표 기능을 코드로 구현하고 실행 로그를 남기세요.
2. `기초 구현` 관점에서 실패 케이스 1개 이상을 재현하고 대응 코드를 추가하세요.
3. 이전 단계 코드와 비교해 변경점(입력/처리/출력)을 3줄로 정리하세요.

## 8) 스스로 점검 체크리스트
- [ ] 조건식이 어떤 불리언 값으로 평가되는지 설명할 수 있다.
- [ ] 분기 누락 없이 `if/elif/else` 경로를 모두 테스트했다.
- [ ] 연산자 우선순위가 헷갈리는 부분에 괄호를 사용해 의도를 명확히 했다.

## 9) 막히면 이렇게 해결해요
1. 에러 메시지 마지막 줄을 먼저 읽어요.
2. 함수 이름과 괄호 짝을 확인해요.
3. `print()`를 넣어 중간 값을 확인해요.
4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

## 10) 학습 후 다음에 배울 내용
- 다음 차시: **class011 / 연산자와 조건문 · 단계 3/4 실전 검증 [class011]** (Day 02 / 3교시)
- 미리보기: 다음 차시 전에 **연산자와 조건문 · 단계 2/4 기초 구현 [class010]** 핵심 코드 1개를 다시 실행해 두면 연산자와 조건문 · 단계 3/4 실전 검증 [class011] 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 조건 분기를 반복문과 결합해 처리량을 늘립니다.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
