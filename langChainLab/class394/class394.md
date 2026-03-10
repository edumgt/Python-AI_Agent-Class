<!-- 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다 -->
# class394 자기주도 학습 가이드

## 1) 오늘의 학습 정보
- 교과목: **Langchain 활용하기**
- 학습 주제: **LangChain 개요 · 단계 2/6 기초 구현 [class394]**
- 세부 시퀀스: **2/56**
- 일정: **Day 50 / 2교시**
- 난이도: **입문**

### 교과목·학습주제 어휘 해설 (IT 강사 스타일)
#### 교과목 표현 분석: `Langchain 활용하기`
- 문법 포인트: 동사 어간 + '-기' 명사형 구조입니다. 학습 행동 자체를 주제로 명사화한 표현입니다.
- 기술 포인트: 체인 기반 워크플로우를 구성해 서비스형 AI를 구현하는 교과목입니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `LangChain` | 고유명사(프레임워크명) | LangChain (한자 없음) | LangChain | LLM 애플리케이션을 체인/도구 기반으로 구성하는 프레임워크입니다. |
| `활용` | 명사/동사 어근 | 활용 (活用) | utilization | 이론이나 도구를 실제 문제 해결 맥락에 적용하는 행위입니다. |

#### 학습주제 표현 분석: `LangChain 개요 · 단계 2/6 기초 구현 [class394]`
- 문법 포인트: 핵심 개념 명사를 중심으로 한 명사구 구조입니다.
- 기술 포인트: 이번 차시는 `LangChain 개요 · 단계 2/6 기초 구현 [class394]` 용어를 중심으로 문제 정의, 코드 구현, 결과 검증까지 연결합니다.
| 용어 | 문법/품사 | 한글·한자 | 영어 | 기술 설명 |
| --- | --- | --- | --- | --- |
| `LangChain` | 고유명사(프레임워크명) | LangChain (한자 없음) | LangChain | LLM 애플리케이션을 체인/도구 기반으로 구성하는 프레임워크입니다. |
| `개요` | 명사(기술 개념어) | 개요 (한자 없음) | (context-specific) | 용어 `개요`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `단계` | 명사(기술 개념어) | 단계 (한자 없음) | (context-specific) | 용어 `단계`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `기초` | 명사(기술 개념어) | 기초 (한자 없음) | (context-specific) | 용어 `기초`: 이번 학습주제에서 정의해야 할 핵심 개념 용어입니다. |
| `구현` | 명사 | 구현 (具現) | implementation | 설계를 실제 코드와 시스템 동작으로 구체화하는 과정입니다. |
| `class394` | 영문 기술명/약어 | class394 (한자 없음) | class394 | 용어 `class394`: 이번 차시에서 쓰이는 핵심 기술 용어입니다. |

## 2) 이전에 배운 내용 (복습)
- 이전 차시: **class393 / LangChain 개요 · 단계 1/6 입문 이해 [class393]** (Day 50 / 1교시)
- 복습 연결: 이전에 배운 **LangChain 개요 · 단계 1/6 입문 이해 [class393]** 를 떠올리며, 오늘 **LangChain 개요 · 단계 2/6 기초 구현 [class394]** 와 어떤 점이 이어지는지 비교해 보세요.

## 3) 주제를 아주 쉽게 이해하기
- 한 줄 설명: LangChain이 왜 필요한지, LLM 앱에서 어떤 역할을 맡는지, 기본 아키텍처를 이해하는 시작 차시입니다.
- 왜 배우나요?: LLM 앱은 프롬프트·메모리·도구·검색·출력 파싱을 함께 다루므로 구성요소를 체계적으로 연결하는 프레임워크가 필요합니다.

### 핵심 개념 3가지
1. `LangChain의 목적`은 LLM 애플리케이션을 모듈 단위로 구성해 재사용성과 확장성을 높이는 것입니다.
2. `왜 필요한가`에 대한 답은 실무에서 단일 호출이 아니라 체인/메모리/도구 조합이 필요하다는 점입니다.
3. `기본 아키텍처`는 입력 -> PromptTemplate -> Model -> Parser -> Memory/Tool/Retriever -> 출력 흐름으로 이해할 수 있습니다.

### 비유로 이해하기
- 샌드위치를 만들 때 재료 준비, 굽기, 포장을 단계별로 나누는 것과 같아요.

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
- 예제 파일: `class394_example1.py`
- 실행 명령:
```bash
python langChainLab/class394/class394_example1.py
```

### example1~example5 단계별 테스트 확장
1. example1: LangChain 목적과 기본 아키텍처를 정리한다.
2. example2: LLM 앱에서 LangChain 역할을 기능별로 매핑한다.
3. example3: 구성요소 연결 실패 케이스를 재현해 점검한다.
4. example4: 아키텍처 개선 전후 흐름을 비교한다.
5. example5: 운영 체크리스트(로그/복구/확장)를 정리한다.

<!-- AUTO-GENERATED: TECH_STACK_FLOW START -->
### 기술 스택
- 언어: `Python 3`
- 실행: `CLI` (`python langChainLab/class394/class394_example1.py`)
- 주요 문법: `체인 단계 함수`, `상태(dict) 전달`, `구성요소 매핑 표`, `실행 로그 출력`
- 학습 포커스: `LangChain 개요 · 단계 2/6 기초 구현 [class394]`

### 실습 example1.py 동작 원리 (Mermaid Flowchart)
```mermaid
flowchart TD
N1["시작: class394 (2/56, 입문)"]
N2["학습 주제 파악: LangChain 개요 · 단계 2/6 기초 구현 [class394]"]
N3["1단계: 요구사항을 체인 기반 구조로 분해한다"]
N4["2단계: 핵심 구성요소를 역할별로 배치한다"]
N5["3단계: 기본 실행 흐름을 연결한다"]
N6["4단계: 구성 요소 간 입출력 계약을 검증한다"]
N7["예제 실행: python langChainLab/class394/class394_example1.py"]
N8["다음 준비: LangChain 개요 · 단계 3/6 응용 확장 [class395] 연결 포인트 정리"]
N1 --> N2
N2 --> N3
N3 --> N4
N4 --> N5
N5 --> N6
N6 --> N7
N7 --> N8
```

### Flow PNG 캡처
![class394 flow](class394_flow.png)
<!-- AUTO-GENERATED: TECH_STACK_FLOW END -->

### 예제 코드를 볼 때 집중할 포인트
1. 단일 함수 호출과 체인 구조의 차이를 명확히 설명하는지 확인하기
2. 구성요소 경계(Model/Prompt/Parser/Memory)가 분리되는지 점검하기
3. 기본 아키텍처가 이후 RAG/Agent 확장과 연결되는지 확인하기

## 6) 퀴즈로 복습하기 (10문항)
- 퀴즈 파일: `class394_quiz.html`
- 브라우저에서 열기:
```bash
langChainLab/class394/class394_quiz.html
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
1. LangChain 없이 구현한 흐름과 LangChain 구성 흐름을 비교해 보세요.
2. 기본 아키텍처 블록(Model, Prompt, Chain, Parser, Memory, Tool, Retriever)을 다이어그램으로 작성하세요.
3. LLM 앱에서 LangChain이 담당하는 역할을 기능별로 매핑하세요.

## 8) 스스로 점검 체크리스트
- [ ] LangChain의 목적과 필요성을 설명할 수 있다.
- [ ] LLM 앱 구성에서 LangChain의 역할을 모듈별로 구분할 수 있다.
- [ ] 기본 아키텍처를 입력→출력 흐름으로 설명할 수 있다.

## 9) 막히면 이렇게 해결해요
1. 에러 메시지 마지막 줄을 먼저 읽어요.
2. 함수 이름과 괄호 짝을 확인해요.
3. `print()`를 넣어 중간 값을 확인해요.
4. 그래도 안 되면 어제 성공한 코드와 한 줄씩 비교해요.

## 10) 학습 후 다음에 배울 내용
- 다음 차시: **class395 / LangChain 개요 · 단계 3/6 응용 확장 [class395]** (Day 50 / 3교시)
- 미리보기: 다음 차시 전에 **LangChain 개요 · 단계 2/6 기초 구현 [class394]** 핵심 코드 1개를 다시 실행해 두면 LangChain 개요 · 단계 3/6 응용 확장 [class395] 학습이 더 쉬워집니다.

## 11) 다음 차시 연결
- 다음 차시에서는 PromptTemplate로 변수 주입형 프롬프트를 재사용 가능하게 설계합니다.
- 오늘 코드를 복사하지 말고, 직접 다시 작성해 보세요.
