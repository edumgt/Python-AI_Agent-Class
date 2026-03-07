<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class028 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **Python 프로그래밍**
- 학습 주제: **파일 입출력**
- 세부 시퀀스: **28/40**
- 일정: **Day 04 / 4교시**
- 난이도: **기초응용**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `Python 프로그래밍`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 코드 문법을 통해 문제를 절차적으로 해결하는 역량을 기르는 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `Python` | 고유명사(언어명) | Python (한자 없음) | Python | 데이터 처리와 AI 실습에 널리 쓰이는 범용 프로그래밍 언어입니다. |
| `프로그래밍` | 명사 | 프로그래밍 (한자 없음) | programming | 문제를 알고리즘으로 분해해 코드로 구현하는 활동입니다. |

#### 학습주제 표현 분석: `파일 입출력`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `파일 입출력` 용어를 중심으로 문제 정의, 코드 구현, 결과 검증까지 연결합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `파일` | 명사(외래어) | 파일 (한자 없음) | file | 디스크에 저장되는 데이터 단위입니다. |
| `입출력` | 명사 | 입출력 (入出力) | input/output | 외부 데이터의 읽기/쓰기 과정을 의미합니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class027 / 파일 입출력** (Day 04 / 3교시)
- 복습 연결: 이전에 배운 **파일 입출력** 를 떠올리며, 오늘 **파일 입출력** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: 메모리 데이터를 파일로 직렬화하고 다시 복원하는 I/O 기본기를 다룹니다.
- 왜 배우나요?: 입출력을 정확히 다루어야 프로그램 상태를 저장하고 외부 시스템과 데이터를 교환할 수 있습니다.

### 핵심 개념 3가지
1. `with open()`은 컨텍스트 매니저로 파일 핸들을 안전하게 열고 자동으로 닫습니다.
2. `인코딩(encoding)`은 문자열과 바이트 변환 규칙으로, 한글 처리에서는 `utf-8` 지정이 중요합니다.
3. `JSON/CSV` 직렬화는 구조화된 데이터를 텍스트 파일로 저장·교환하는 표준 방식입니다.

### 비유로 이해하기
- 노트를 읽고 쓰되 반드시 책을 닫아 보관하는 문서 관리 절차와 같습니다.

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
- 예제 파일: `class028_example.py`
- 실행 명령:
```bash
python pyBasics/class028/class028_example.py
```


<!-- AUTO-GENERATED: OS_COMMANDS START -->
## 5-1) 운영체제별 실행 명령 예시
### PowerShell (Windows)
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python .\pyBasics\class028\class028.py
python .\pyBasics\class028\class028_example.py
python .\pyBasics\class028\class028_assignment.py
start .\pyBasics\class028\class028_quiz.html
```

### WSL Ubuntu (bash)
```bash
cd /mnt/c/DevOps/Python-AI_Agent-Class
python3 pyBasics/class028/class028.py
python3 pyBasics/class028/class028_example.py
python3 pyBasics/class028/class028_assignment.py
explorer.exe "$(wslpath -w 'pyBasics/class028/class028_quiz.html')"
```

### run_class/run_day 스크립트 연동 (WSL bash)
```bash
./run_class.sh class028
./run_day.sh 4 launcher
```
<!-- AUTO-GENERATED: OS_COMMANDS END -->

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python pyBasics/class028/class028_example.py`)
- 주요 문법: `with open()`, `read/write`, `인코딩(utf-8)`, `json/csv`
- 학습 포커스: `파일 입출력`

### 실습 example.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class028 (28/40, 기초응용)"]
N2["학습 주제 파악: 파일 입출력"]
N3["1단계: 입출력 파일 경로와 모드를 정의한다"]
N4["2단계: 파일을 읽어 데이터 구조로 파싱한다"]
N5["3단계: 처리 결과를 파일로 직렬화해 저장한다"]
N6["4단계: 저장/재로딩 검증으로 데이터 무결성을 확인한다"]
N7["예제 실행: python pyBasics/class028/class028_example.py"]
N8["다음 준비: 예외처리와 디버깅 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class028 flow](class028_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 파일 열기 모드와 인코딩이 요구사항과 맞는지 확인하기
2. 입출력 전후 데이터 구조가 보존되는지 검증하기
3. 파일 미존재/권한 오류를 대비한 예외 처리가 있는지 점검하기

## 6) 퀴즈로 복습하기 (5문항)
- 퀴즈 파일: `class028_quiz.html`
- 브라우저에서 열기:
```bash
pyBasics/class028/class028_quiz.html
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
1. `with open(..., encoding='utf-8')`으로 텍스트 파일 읽기/쓰기를 실습하세요.
2. 리스트/딕셔너리를 JSON으로 저장하고 다시 로드해 동일성 여부를 확인하세요.
3. 없는 파일 경로를 의도적으로 실행해 예외 메시지를 확인하세요.

## 8) 스스로 점검 체크리스트
- [ ] 파일 경로, 모드(`r/w/a`), 인코딩 의미를 설명할 수 있다.
- [ ] 저장한 데이터와 로드한 데이터의 일치 여부를 검증했다.
- [ ] 입출력 실패 시 예외 처리 흐름을 포함했다.

## 9) 막히면 이렇게 해결해요
1. 에러 메시지 마지막 줄을 먼저 읽어요.
2. 함수 이름과 괄호 짝을 확인해요.
3. `print()`를 넣어 중간 값을 확인해요.
4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

## 10) 학습 후 다음에 배울 내용
- 다음 차시: **class029 / 예외처리와 디버깅** (Day 04 / 5교시)
- 미리보기: 다음 차시 전에 **파일 입출력** 핵심 코드 1개를 다시 실행해 두면 예외처리와 디버깅 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 파일/네트워크 오류를 안정적으로 다루는 예외처리를 심화합니다.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
