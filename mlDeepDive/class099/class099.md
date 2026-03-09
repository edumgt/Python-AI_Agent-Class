<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class099 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **머신러닝과 딥러닝**
- 학습 주제: **분류 모델 · 단계 4/5 실전 검증 [class099]**
- 학습 주제 진행: **분류 모델 · 단계 4/5 실전 검증 [class099] (총 5시간 중 4시간차)**
- 세부 시퀀스: **19/48**
- 일정: **Day 13 / 3교시**
- 최종 목표: **Agent 폴더의 실제 시스템 구성요소를 구현·연동·운영할 수 있는 개발자 역량 확보**
- 난이도: **기초응용**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `머신러닝과 딥러닝`
- 문법 포인트: 명사와 명사를 대등하게 묶는 병렬 명사구 구조입니다.
- 기술 포인트: 모델 학습과 성능 평가를 통해 예측 시스템을 설계하는 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `머신러닝` | 명사(외래어) | 머신러닝 (한자 없음) | machine learning | 데이터에서 패턴을 학습해 예측 규칙을 만드는 기술입니다. |
| `딥러닝` | 명사(외래어) | 딥러닝 (한자 없음) | deep learning | 다층 신경망으로 복잡한 패턴을 학습하는 머신러닝 하위 분야입니다. |

#### 학습주제 표현 분석: `분류 모델 · 단계 4/5 실전 검증 [class099]`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `분류 모델 · 단계 4/5 실전 검증 [class099]`를 중심으로 같은 주제 내에서 단계적으로 고도화된 구현을 수행합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `분류` | 명사 | 분류 (分類) | classification | 입력을 사전 정의된 카테고리로 할당하는 지도학습 과제입니다. |
| `모델` | 명사(외래어) | 모델 (한자 없음) | model | 입력과 출력 관계를 수학적으로 근사한 계산 구조입니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class098 / 분류 모델 · 단계 3/5 응용 확장 [class098]** (Day 13 / 2교시)
- 복습 연결: 이전에 배운 **분류 모델 · 단계 3/5 응용 확장 [class098]** 를 떠올리며, 오늘 **분류 모델 · 핵심 구현 리팩터링 적용 (차시 19) [class099]** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: 분류 모델를 단계 4/5(실전 검증) 수준으로 고도화해 구현하는 차시입니다.
- 왜 배우나요?: 동일 주제를 반복하더라도 단계별 난이도를 높여 실무 수준의 문제 해결력을 만들기 위해서입니다.

### 핵심 개념 3가지
1. `분류 모델`의 핵심 입력/출력 구조를 단계 4/5 기준으로 명확히 정의합니다.
2. `실전 검증` 수준에서 필요한 구현 패턴(검증, 예외, 로깅, 성능)을 코드에 반영합니다.
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
- 예제 파일: `class099_example1.py`
- 실행 명령:
```bash
python mlDeepDive/class099/class099_example1.py
```


<!-- AUTO-GENERATED: OS_COMMANDS START -->
## 5-1) 운영체제별 실행 명령 예시
### PowerShell (Windows)
```powershell
cd C:\DevOps\Python-AI_Agent-Class
python .\mlDeepDive\class099\class099.py
python .\mlDeepDive\class099\class099_example1.py
python .\mlDeepDive\class099\class099_assignment.py
start .\mlDeepDive\class099\class099_quiz.html
```

### WSL Ubuntu (bash)
```bash
cd /mnt/c/DevOps/Python-AI_Agent-Class
python3 mlDeepDive/class099/class099.py
python3 mlDeepDive/class099/class099_example1.py
python3 mlDeepDive/class099/class099_assignment.py
explorer.exe "$(wslpath -w 'mlDeepDive/class099/class099_quiz.html')"
```

### run_class/run_day 스크립트 연동 (WSL bash)
```bash
./run_class.sh class099
./run_day.sh 13 launcher
```
<!-- AUTO-GENERATED: OS_COMMANDS END -->

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python mlDeepDive/class099/class099_example1.py`)
- 주요 문법: `함수`, `리스트 컴프리헨션`, `오차 계산`, `출력(print)`
- 학습 포커스: `분류 모델 · 단계 4/5 실전 검증 [class099]`

### 실습 example1.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class099 (19/48, 기초응용)"]
N2["학습 주제 파악: 분류 모델 · 단계 4/5 실전 검증 [class099]"]
N3["1단계: 학습 데이터(X,y)를 준비한다"]
N4["2단계: 예측 규칙(모델)을 학습/계산한다"]
N5["3단계: 오차 지표를 계산해 성능을 확인한다"]
N6["4단계: 오차 원인을 분석해 개선 포인트를 정리한다"]
N7["예제 실행: python mlDeepDive/class099/class099_example1.py"]
N8["다음 준비: 분류 모델 · 단계 4/5 실전 검증 [class099] 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class099 flow](class099_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 입력이 무엇인지 먼저 찾기
2. 처리 규칙(함수/조건/반복) 확인하기
3. 출력 결과가 목표와 맞는지 점검하기

## 6) 퀴즈로 복습하기 (5문항)
- 퀴즈 파일: `class099_quiz.html`
- 브라우저에서 열기:
```bash
mlDeepDive/class099/class099_quiz.html
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
1. `분류 모델` 단계 4/5 목표 기능을 코드로 구현하고 실행 로그를 남기세요.
2. `실전 검증` 관점에서 실패 케이스 1개 이상을 재현하고 대응 코드를 추가하세요.
3. 이전 단계 코드와 비교해 변경점(입력/처리/출력)을 3줄로 정리하세요.

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
- 다음 차시: **class100 / 분류 모델 · 단계 5/5 운영 최적화 [class100]** (Day 13 / 4교시)
- 미리보기: 다음 차시 전에 **분류 모델 · 단계 4/5 실전 검증 [class099]** 핵심 코드 1개를 다시 실행해 두면 분류 모델 · 단계 5/5 운영 최적화 [class100] 학습이 더 쉬워집니다.


## 12) ML/DL Docker + MLOps/AIOps 실습 연결
- 실사례 이미지: `pytorch/pytorch`, `tensorflow/serving`, `ghcr.io/mlflow/mlflow`
- 확장 실습: 학습 컨테이너 생성 → 추론 API 서빙 → 메트릭 수집(Prometheus) → 대시보드(Grafana)
- 운영 점검: 모델 버전, 배포 이력, 실패 시 롤백 절차를 기록해 Agent 시스템 운영 관점으로 연결

## 11) 다음 차시 연결
- 다음 차시에서는 더 정확한 예측을 위해 특징(feature)을 늘려 볼 거예요.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
