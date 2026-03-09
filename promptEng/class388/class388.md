<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class388 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **프롬프트 엔지니어링**
- 학습 주제: **도메인 템플릿 작성 · 단계 4/4 운영 최적화 [class388]**
- 학습 주제 진행: **도메인 템플릿 작성 · 단계 4/4 운영 최적화 [class388] (총 4시간 중 4시간차)**
- 세부 시퀀스: **36/40**
- 일정: **Day 49 / 4교시**
- 최종 목표: **Agent 폴더의 실제 시스템 구성요소를 구현·연동·운영할 수 있는 개발자 역량 확보**
- 난이도: **실전심화**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `프롬프트 엔지니어링`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 프롬프트 설계로 모델 응답 품질을 제어하는 생성형 AI 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `프롬프트` | 명사(외래어) | 프롬프트 (한자 없음) | prompt | 모델의 응답 방향을 결정하는 입력 지시문입니다. |
| `엔지니어링` | 명사(외래어) | 엔지니어링 (한자 없음) | engineering | 재현 가능한 품질을 목표로 설계·검증하는 공학적 접근입니다. |

#### 학습주제 표현 분석: `도메인 템플릿 작성 · 단계 4/4 운영 최적화 [class388]`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `도메인 템플릿 작성 · 단계 4/4 운영 최적화 [class388]`를 중심으로 같은 주제 내에서 단계적으로 고도화된 구현을 수행합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `도메인` | 명사(외래어) | 도메인 (한자 없음) | domain | 문제를 푸는 특정 업무 영역(예: 의료, 법률, 제조)을 뜻합니다. |
| `템플릿` | 명사(기술 개념어) | 템플릿 (한자 없음) | (context-specific) | 용어 `템플릿`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `작성` | 명사(기술 개념어) | 작성 (한자 없음) | (context-specific) | 용어 `작성`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class387 / 도메인 템플릿 작성 · 단계 3/4 실전 검증 [class387]** (Day 49 / 3교시)
- 복습 연결: 이전에 배운 **도메인 템플릿 작성 · 단계 3/4 실전 검증 [class387]** 를 떠올리며, 오늘 **도메인 템플릿 작성 · 운영 확장 모니터링 지표 연결 (차시 36) [class388]** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: 도메인 템플릿 작성를 단계 4/4(운영 최적화) 수준으로 고도화해 구현하는 차시입니다.
- 왜 배우나요?: 동일 주제를 반복하더라도 단계별 난이도를 높여 실무 수준의 문제 해결력을 만들기 위해서입니다.

### 핵심 개념 3가지
1. `도메인 템플릿 작성`의 핵심 입력/출력 구조를 단계 4/4 기준으로 명확히 정의합니다.
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
- 예제 파일: `class388_example1.py`
- 실행 명령:
```bash
python promptEng/class388/class388_example1.py
```


<!-- AUTO-GENERATED: OS_COMMANDS START -->
## 5-1) 운영체제별 실행 명령 예시
### PowerShell (Windows)
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python .\promptEng\class388\class388.py
python .\promptEng\class388\class388_example1.py
python .\promptEng\class388\class388_assignment.py
start .\promptEng\class388\class388_quiz.html
```

### WSL Ubuntu (bash)
```bash
cd /mnt/c/DevOps/Python-AI_Agent-Class
python3 promptEng/class388/class388.py
python3 promptEng/class388/class388_example1.py
python3 promptEng/class388/class388_assignment.py
explorer.exe "$(wslpath -w 'promptEng/class388/class388_quiz.html')"
```

### run_class/run_day 스크립트 연동 (WSL bash)
```bash
./run_class.sh class388
./run_day.sh 49 launcher
```
<!-- AUTO-GENERATED: OS_COMMANDS END -->

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python promptEng/class388/class388_example1.py`)
- 주요 문법: `문자열 템플릿`, `함수`, `변수 치환`, `출력(print)`
- 학습 포커스: `도메인 템플릿 작성 · 단계 4/4 운영 최적화 [class388]`

### 실습 example1.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class388 (36/40, 실전심화)"]
N2["학습 주제 파악: 도메인 템플릿 작성 · 단계 4/4 운영 최적화 [class388]"]
N3["1단계: 역할/목표/형식을 명확히 정의한다"]
N4["2단계: 프롬프트 템플릿을 작성한다"]
N5["3단계: 예시를 바꿔 응답 품질을 비교한다"]
N6["4단계: 평가 기준에 맞게 프롬프트를 튜닝한다"]
N7["예제 실행: python promptEng/class388/class388_example1.py"]
N8["다음 준비: 도메인 템플릿 작성 · 단계 4/4 운영 최적화 [class388] 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class388 flow](class388_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 입력이 무엇인지 먼저 찾기
2. 처리 규칙(함수/조건/반복) 확인하기
3. 출력 결과가 목표와 맞는지 점검하기

## 6) 퀴즈로 복습하기 (5문항)
- 퀴즈 파일: `class388_quiz.html`
- 브라우저에서 열기:
```bash
promptEng/class388/class388_quiz.html
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
1. `도메인 템플릿 작성` 단계 4/4 목표 기능을 코드로 구현하고 실행 로그를 남기세요.
2. `운영 최적화` 관점에서 실패 케이스 1개 이상을 재현하고 대응 코드를 추가하세요.
3. 이전 단계 코드와 비교해 변경점(입력/처리/출력)을 3줄로 정리하세요.

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
- 다음 차시: **class389 / 실전 프롬프트 튜닝 · 단계 1/4 입문 이해 [class389]** (Day 49 / 5교시)
- 미리보기: 다음 차시 전에 **도메인 템플릿 작성 · 단계 4/4 운영 최적화 [class388]** 핵심 코드 1개를 다시 실행해 두면 실전 프롬프트 튜닝 · 단계 1/4 입문 이해 [class389] 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 프롬프트를 체인으로 묶어 복잡한 작업을 수행해요.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
