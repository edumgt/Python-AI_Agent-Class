<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class373 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **프롬프트 엔지니어링**
- 학습 주제: **단계적 추론 유도**
- 세부 시퀀스: **21/40**
- 일정: **Day 47 / 5교시**
- 난이도: **기초응용**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `프롬프트 엔지니어링`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 프롬프트 설계로 모델 응답 품질을 제어하는 생성형 AI 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `프롬프트` | 명사(외래어) | 프롬프트 (한자 없음) | prompt | 모델의 응답 방향을 결정하는 입력 지시문입니다. |
| `엔지니어링` | 명사(외래어) | 엔지니어링 (한자 없음) | engineering | 재현 가능한 품질을 목표로 설계·검증하는 공학적 접근입니다. |

#### 학습주제 표현 분석: `단계적 추론 유도`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `단계적 추론 유도` 용어를 중심으로 문제 정의, 코드 구현, 결과 검증까지 연결합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `단계적` | 명사(기술 개념어) | 단계적 (한자 없음) | (context-specific) | 용어 `단계적`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `추론` | 명사(기술 개념어) | 추론 (한자 없음) | (context-specific) | 용어 `추론`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `유도` | 명사(기술 개념어) | 유도 (한자 없음) | (context-specific) | 용어 `유도`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class372 / 예시 기반 학습** (Day 47 / 4교시)
- 복습 연결: 이전에 배운 **예시 기반 학습** 를 떠올리며, 오늘 **단계적 추론 유도** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: 좋은 질문(프롬프트)을 설계해서 AI 답변 품질을 높이는 방법을 배워요.
- 왜 배우나요?: 같은 AI라도 질문 방식이 다르면 답변 품질이 크게 달라져요.

### 핵심 개념 3가지
1. 역할(role), 목표(goal), 형식(format)을 명확히 쓰면 답이 좋아져요.
2. 입력 변수를 분리하면 재사용 가능한 템플릿이 돼요.
3. 평가 기준을 먼저 정하면 결과를 고치기 쉬워요.

### 비유로 이해하기
- 친구에게 길을 물을 때 목적지와 조건을 정확히 말해야 정확한 답을 듣는 것과 같아요.

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
- 예제 파일: `class373_example.py`
- 실행 명령:
```bash
python promptEng/class373/class373_example.py
```


<!-- AUTO-GENERATED: OS_COMMANDS START -->
## 5-1) 운영체제별 실행 명령 예시
### PowerShell (Windows)
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python .\promptEng\class373\class373.py
python .\promptEng\class373\class373_example.py
python .\promptEng\class373\class373_assignment.py
start .\promptEng\class373\class373_quiz.html
```

### WSL Ubuntu (bash)
```bash
cd /mnt/c/DevOps/Python-AI_Agent-Class
python3 promptEng/class373/class373.py
python3 promptEng/class373/class373_example.py
python3 promptEng/class373/class373_assignment.py
explorer.exe "$(wslpath -w 'promptEng/class373/class373_quiz.html')"
```

### run_class/run_day 스크립트 연동 (WSL bash)
```bash
./run_class.sh class373
./run_day.sh 47 launcher
```
<!-- AUTO-GENERATED: OS_COMMANDS END -->

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python promptEng/class373/class373_example.py`)
- 주요 문법: `문자열 템플릿`, `함수`, `변수 치환`, `출력(print)`
- 학습 포커스: `단계적 추론 유도`

### 실습 example.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class373 (21/40, 기초응용)"]
N2["학습 주제 파악: 단계적 추론 유도"]
N3["1단계: 역할/목표/형식을 명확히 정의한다"]
N4["2단계: 프롬프트 템플릿을 작성한다"]
N5["3단계: 예시를 바꿔 응답 품질을 비교한다"]
N6["4단계: 평가 기준에 맞게 프롬프트를 튜닝한다"]
N7["예제 실행: python promptEng/class373/class373_example.py"]
N8["다음 준비: 단계적 추론 유도 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class373 flow](class373_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 입력이 무엇인지 먼저 찾기
2. 처리 규칙(함수/조건/반복) 확인하기
3. 출력 결과가 목표와 맞는지 점검하기

## 6) 퀴즈로 복습하기 (5문항)
- 퀴즈 파일: `class373_quiz.html`
- 브라우저에서 열기:
```bash
promptEng/class373/class373_quiz.html
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
1. 예제 템플릿에서 역할과 질문을 바꿔 실행해 봐요.
2. 답변 형식을 3줄 요약으로 제한해 봐요.
3. 좋은 프롬프트와 나쁜 프롬프트를 한 쌍 비교해 봐요.

## 8) 스스로 점검 체크리스트
- [ ] 역할/목표/형식을 각각 설명할 수 있다.
- [ ] 템플릿 변수 2개 이상을 직접 바꿨다.
- [ ] 출력 품질이 왜 달라졌는지 설명할 수 있다.

## 9) 막히면 이렇게 해결해요
1. 에러 메시지 마지막 줄을 먼저 읽어요.
2. 함수 이름과 괄호 짝을 확인해요.
3. `print()`를 넣어 중간 값을 확인해요.
4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

## 10) 학습 후 다음에 배울 내용
- 다음 차시: **class374 / 단계적 추론 유도** (Day 47 / 6교시)
- 미리보기: 다음 차시 전에 **단계적 추론 유도** 핵심 코드 1개를 다시 실행해 두면 단계적 추론 유도 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 프롬프트를 체인으로 묶어 복잡한 작업을 수행해요.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
