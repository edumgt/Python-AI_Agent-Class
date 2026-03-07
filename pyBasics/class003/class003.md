<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class003 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **Python 프로그래밍**
- 학습 주제: **오리엔테이션 및 개발환경 준비**
- 세부 시퀀스: **3/40**
- 일정: **Day 01 / 3교시**
- 난이도: **입문**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `Python 프로그래밍`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 코드 문법을 통해 문제를 절차적으로 해결하는 역량을 기르는 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `Python` | 고유명사(언어명) | Python (한자 없음) | Python | 데이터 처리와 AI 실습에 널리 쓰이는 범용 프로그래밍 언어입니다. |
| `프로그래밍` | 명사 | 프로그래밍 (한자 없음) | programming | 문제를 알고리즘으로 분해해 코드로 구현하는 활동입니다. |

#### 학습주제 표현 분석: `오리엔테이션 및 개발환경 준비`
- 문법 포인트: 명사구를 연결어 '및'으로 병렬 연결한 구조입니다. 동등한 학습 범위를 함께 제시합니다.
- 기술 포인트: 이번 차시는 `오리엔테이션 및 개발환경 준비` 용어를 중심으로 문제 정의, 코드 구현, 결과 검증까지 연결합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `오리엔테이션` | 명사(기술 개념어) | 오리엔테이션 (한자 없음) | (context-specific) | 용어 `오리엔테이션`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `개발환경` | 명사(기술 개념어) | 개발환경 (한자 없음) | (context-specific) | 용어 `개발환경`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `준비` | 명사(기술 개념어) | 준비 (한자 없음) | (context-specific) | 용어 `준비`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class002 / 오리엔테이션 및 개발환경 준비** (Day 01 / 2교시)
- 복습 연결: 이전에 배운 **오리엔테이션 및 개발환경 준비** 를 떠올리며, 오늘 **오리엔테이션 및 개발환경 준비** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: Python 코드가 어떤 실행환경에서 동작하는지 먼저 맞추는 차시입니다.
- 왜 배우나요?: 인터프리터, 가상환경, 패키지 의존성을 이해해야 이후 변수·함수·클래스 실습 결과를 재현할 수 있습니다.

### 핵심 개념 3가지
1. `인터프리터`는 소스 코드를 해석해 실행하며 `python 파일.py`가 기본 실행 경로입니다.
2. `가상환경(venv)`은 프로젝트별 라이브러리를 분리해 버전 충돌을 막는 실행 격리층입니다.
3. `requirements.txt`는 의존성 버전을 고정해 팀/장비가 달라도 동일한 환경을 재구성하게 해줍니다.

### 비유로 이해하기
- 실험 전에 실험대와 장비를 먼저 교정하는 준비 단계와 같습니다.

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
- 예제 파일: `class003_example.py`
- 실행 명령:
```bash
python pyBasics/class003/class003_example.py
```


<!-- AUTO-GENERATED: OS_COMMANDS START -->
## 5-1) 운영체제별 실행 명령 예시
### PowerShell (Windows)
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python .\pyBasics\class003\class003.py
python .\pyBasics\class003\class003_example.py
python .\pyBasics\class003\class003_assignment.py
start .\pyBasics\class003\class003_quiz.html
```

### WSL Ubuntu (bash)
```bash
cd /mnt/c/DevOps/Python-AI_Agent-Class
python3 pyBasics/class003/class003.py
python3 pyBasics/class003/class003_example.py
python3 pyBasics/class003/class003_assignment.py
explorer.exe "$(wslpath -w 'pyBasics/class003/class003_quiz.html')"
```

### run_class/run_day 스크립트 연동 (WSL bash)
```bash
./run_class.sh class003
./run_day.sh 1 launcher
```
<!-- AUTO-GENERATED: OS_COMMANDS END -->

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python pyBasics/class003/class003_example.py`)
- 주요 문법: `모듈 import`, `변수 할당`, `실행 진입점(__name__)`, `출력(print)`
- 학습 포커스: `오리엔테이션 및 개발환경 준비`

### 실습 example.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class003 (3/40, 입문)"]
N2["학습 주제 파악: 오리엔테이션 및 개발환경 준비"]
N3["1단계: Python 인터프리터 버전과 실행 경로를 확인한다"]
N4["2단계: 가상환경을 만들고 의존성 패키지를 설치한다"]
N5["3단계: 샘플 스크립트를 실행해 런타임 동작을 검증한다"]
N6["4단계: 실행 오류 메시지를 읽고 환경 설정을 수정한다"]
N7["예제 실행: python pyBasics/class003/class003_example.py"]
N8["다음 준비: 오리엔테이션 및 개발환경 준비 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class003 flow](class003_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 코드가 `__name__ == "__main__"` 블록에서 시작되는지 확인하기
2. 현재 터미널의 인터프리터가 프로젝트 `.venv`인지 확인하기
3. 필수 패키지 import 테스트로 실행환경을 검증하기

## 6) 퀴즈로 복습하기 (5문항)
- 퀴즈 파일: `class003_quiz.html`
- 브라우저에서 열기:
```bash
pyBasics/class003/class003_quiz.html
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
1. `python --version`과 `where python`으로 현재 인터프리터 경로를 확인하세요.
2. `python -m venv .venv` 후 활성화하고 `pip install -r requirements.txt`를 실행하세요.
3. 샘플 코드를 실행하고 `ModuleNotFoundError`가 나면 인터프리터/패키지 경로를 점검하세요.

## 8) 스스로 점검 체크리스트
- [ ] 전역 Python과 프로젝트 `.venv`의 차이를 설명할 수 있다.
- [ ] 가상환경 생성/활성화/비활성화 과정을 스스로 재현할 수 있다.
- [ ] `requirements.txt`의 의미(재현 가능한 환경)를 설명할 수 있다.

## 9) 막히면 이렇게 해결해요
1. 에러 메시지 마지막 줄을 먼저 읽어요.
2. 함수 이름과 괄호 짝을 확인해요.
3. `print()`를 넣어 중간 값을 확인해요.
4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

## 10) 학습 후 다음에 배울 내용
- 다음 차시: **class004 / 오리엔테이션 및 개발환경 준비** (Day 01 / 4교시)
- 미리보기: 다음 차시 전에 **오리엔테이션 및 개발환경 준비** 핵심 코드 1개를 다시 실행해 두면 오리엔테이션 및 개발환경 준비 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 준비된 환경에서 변수·상수·타입을 다루며 PL 기본기를 시작합니다.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
