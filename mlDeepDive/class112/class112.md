<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class112 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **머신러닝과 딥러닝**
- 학습 주제: **과적합과 일반화**
- 세부 시퀀스: **32/48**
- 일정: **Day 14 / 8교시**
- 난이도: **기초응용**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `머신러닝과 딥러닝`
- 문법 포인트: 명사와 명사를 대등하게 묶는 병렬 명사구 구조입니다.
- 기술 포인트: 모델 학습과 성능 평가를 통해 예측 시스템을 설계하는 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `머신러닝` | 명사(외래어) | 머신러닝 (한자 없음) | machine learning | 데이터에서 패턴을 학습해 예측 규칙을 만드는 기술입니다. |
| `딥러닝` | 명사(외래어) | 딥러닝 (한자 없음) | deep learning | 다층 신경망으로 복잡한 패턴을 학습하는 머신러닝 하위 분야입니다. |

#### 학습주제 표현 분석: `과적합과 일반화`
- 문법 포인트: 명사와 명사를 대등하게 묶는 병렬 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `과적합과 일반화` 용어를 중심으로 문제 정의, 코드 구현, 결과 검증까지 연결합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `과적합` | 명사 | 과적합 (過適合) | overfitting | 학습 데이터에 과도하게 맞춰 일반화 성능이 떨어지는 현상입니다. |
| `일반화` | 명사 | 일반화 (一般化) | generalization | 보지 못한 데이터에서도 성능을 유지하는 모델 능력입니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class111 / 과적합과 일반화** (Day 14 / 7교시)
- 복습 연결: 이전에 배운 **과적합과 일반화** 를 떠올리며, 오늘 **과적합과 일반화** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: 데이터를 보고 규칙을 찾는 '작은 모델' 사고법을 배워요.
- 왜 배우나요?: 정답을 외우는 대신 규칙을 찾으면 새로운 문제도 스스로 예측할 수 있어요.

### 핵심 개념 3가지
1. 모델은 입력을 받아 예측값을 만들어요.
2. 예측값과 실제값의 차이(오차)를 확인해야 실력이 늘어요.
3. 작은 데이터로 원리를 이해한 뒤 큰 데이터로 확장해요.

### 비유로 이해하기
- 농구 슛 연습에서 '던진 거리와 결과'를 보고 감을 조절하는 것과 비슷해요.

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
- 예제 파일: `class112_example.py`
- 실행 명령:
```bash
python mlDeepDive/class112/class112_example.py
```


<!-- AUTO-GENERATED: OS_COMMANDS START -->
## 5-1) 운영체제별 실행 명령 예시
### PowerShell (Windows)
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python .\mlDeepDive\class112\class112.py
python .\mlDeepDive\class112\class112_example.py
python .\mlDeepDive\class112\class112_assignment.py
start .\mlDeepDive\class112\class112_quiz.html
```

### WSL Ubuntu (bash)
```bash
cd /mnt/c/DevOps/Python-AI_Agent-Class
python3 mlDeepDive/class112/class112.py
python3 mlDeepDive/class112/class112_example.py
python3 mlDeepDive/class112/class112_assignment.py
explorer.exe "$(wslpath -w 'mlDeepDive/class112/class112_quiz.html')"
```

### run_class/run_day 스크립트 연동 (WSL bash)
```bash
./run_class.sh class112
./run_day.sh 14 launcher
```
<!-- AUTO-GENERATED: OS_COMMANDS END -->

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python mlDeepDive/class112/class112_example.py`)
- 주요 문법: `함수`, `리스트 컴프리헨션`, `오차 계산`, `출력(print)`
- 학습 포커스: `과적합과 일반화`

### 실습 example.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class112 (32/48, 기초응용)"]
N2["학습 주제 파악: 과적합과 일반화"]
N3["1단계: 학습 데이터(X,y)를 준비한다"]
N4["2단계: 예측 규칙(모델)을 학습/계산한다"]
N5["3단계: 오차 지표를 계산해 성능을 확인한다"]
N6["4단계: 오차 원인을 분석해 개선 포인트를 정리한다"]
N7["예제 실행: python mlDeepDive/class112/class112_example.py"]
N8["다음 준비: 과적합과 일반화 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class112 flow](class112_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 입력이 무엇인지 먼저 찾기
2. 처리 규칙(함수/조건/반복) 확인하기
3. 출력 결과가 목표와 맞는지 점검하기

## 6) 퀴즈로 복습하기 (5문항)
- 퀴즈 파일: `class112_quiz.html`
- 브라우저에서 열기:
```bash
mlDeepDive/class112/class112_quiz.html
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
1. 예제의 입력/정답 쌍을 먼저 표처럼 정리해 봐요.
2. 평균 기반 예측처럼 가장 쉬운 모델부터 실행해 봐요.
3. 오차가 큰 항목을 찾아 이유를 한 문장으로 적어 봐요.

## 8) 스스로 점검 체크리스트
- [ ] 입력값과 정답값의 의미를 설명할 수 있다.
- [ ] 예측 결과와 오차를 직접 확인했다.
- [ ] 오차를 줄이기 위한 아이디어를 1개 이상 말했다.

## 9) 막히면 이렇게 해결해요
1. 에러 메시지 마지막 줄을 먼저 읽어요.
2. 함수 이름과 괄호 짝을 확인해요.
3. `print()`를 넣어 중간 값을 확인해요.
4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

## 10) 학습 후 다음에 배울 내용
- 다음 차시: **class113 / 과적합과 일반화** (Day 15 / 1교시)
- 미리보기: 다음 차시 전에 **과적합과 일반화** 핵심 코드 1개를 다시 실행해 두면 과적합과 일반화 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 더 정확한 예측을 위해 특징(feature)을 늘려 볼 거예요.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
