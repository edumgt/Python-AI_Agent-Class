# LangChain, LangGraph 정리 가이드

## 1. 개요

LangChain과 LangGraph는 **LLM 기반 애플리케이션과 AI Agent를 만들기 위한 프레임워크**입니다.

가장 간단히 정리하면:

- **LangChain**: LLM 앱을 빠르게 만들기 위한 상위 프레임워크
- **LangGraph**: 상태(state)와 흐름(flow)을 정교하게 제어하는 그래프 기반 오케스트레이션 프레임워크

실무에서는 둘을 경쟁 제품처럼 보기보다, **함께 쓰는 관계**로 보는 것이 더 정확합니다.

---

## 2. LangChain이란?

LangChain은 LLM을 활용한 애플리케이션을 쉽게 만들기 위한 프레임워크입니다.

주요 역할:

- LLM 연결
- 프롬프트 구성
- Tool 연결
- 문서 검색(RAG)
- Agent 구성
- 다양한 모델 공급자 교체를 쉽게 처리

즉, LangChain은 다음과 같은 흐름을 빠르게 구현하게 도와줍니다.

```text
사용자 질문 -> 검색/도구 호출 -> LLM 응답 생성
```

### LangChain이 잘 맞는 경우

- 사내 문서 챗봇
- FAQ 봇
- RAG 시스템
- 빠른 프로토타입
- 간단한 Tool Calling Agent

### LangChain의 장점

- 빠르게 시작 가능
- 추상화 수준이 높음
- 모델/툴/프롬프트/RAG 구성이 쉬움

### LangChain의 한계

복잡한 분기, 재시도, 장기 실행, 상태 복구, 승인 플로우 등이 많아지면 제어가 어려워질 수 있습니다. 이때 LangGraph가 필요해집니다.

---

## 3. LangGraph란?

LangGraph는 상태 기반의 Agent Workflow를 설계하는 프레임워크입니다.

핵심 개념:

- **State**: 현재 작업 상태
- **Node**: 실제 작업 단위
- **Edge**: 다음 단계로 연결되는 흐름
- **Conditional Edge**: 조건에 따라 다음 노드 분기

즉, 아래 같은 구조를 설계할 수 있습니다.

```text
START -> classify -> (weather/general) -> END
```

또는 더 복잡하게:

```text
질문 수신
-> 분류
-> 문서 검색 또는 API 호출
-> 검증
-> 사람 승인
-> 최종 응답
```

### LangGraph가 잘 맞는 경우

- 상태 저장이 중요한 Agent
- 복잡한 조건 분기
- 사람 승인(Human-in-the-loop)
- 작업 중단 후 재개
- 장기 실행 워크플로
- 멀티 Agent 시스템

### LangGraph의 장점

- 흐름 제어가 정교함
- 상태 관리가 명확함
- 복구/재개에 유리
- 실무형 Agent 설계에 적합

---

## 4. LangChain vs LangGraph

| 항목 | LangChain | LangGraph |
|---|---|---|
| 목적 | LLM 앱 빠른 개발 | 상태 기반 Agent 흐름 설계 |
| 추상화 수준 | 높음 | 더 낮음 |
| 장점 | 빠른 개발, 쉬운 시작 | 복잡한 제어, 분기, 복구 |
| 적합한 대상 | 챗봇, RAG, 간단한 Agent | 운영형 Agent, 복잡한 Workflow |
| 사고 방식 | 모델/툴 조립 | 상태와 흐름 설계 |

### 관계 정리

- LangChain은 빠른 생산성을 위한 프레임워크
- LangGraph는 더 세밀한 흐름 제어를 위한 프레임워크
- 현재 LangChain Agent는 내부적으로 LangGraph 기반 런타임 개념과 연결되어 설명되는 경우가 많습니다.

---

## 5. 다른 도구들과 비교

## 5-1. LangGraph vs AWS Step Functions

둘 다 흐름을 제어하지만 대상이 다릅니다.

### LangGraph
- AI Agent 내부 추론 흐름 제어
- 상태 기반 판단
- Tool 호출, 검색, 승인, 재개에 적합

### Step Functions
- AWS 서비스 오케스트레이션
- Lambda, ECS, DynamoDB, SNS 등을 순서대로 연결
- 백엔드 비즈니스 프로세스에 강함

### 쉽게 구분

- **LangGraph**: AI의 생각 흐름
- **Step Functions**: 클라우드 서비스 실행 흐름

---

## 5-2. LangGraph vs Airflow

### Airflow
- DAG 기반
- 배치/ETL/스케줄링에 강함
- 정기 작업 실행에 적합

### LangGraph
- 실시간 Agent 흐름 제어
- 사용자 입력에 따라 동적으로 분기
- 상태 기반 의사결정에 적합

### 쉽게 구분

- **Airflow**: 정해진 데이터 파이프라인
- **LangGraph**: 상태에 따라 달라지는 Agent Workflow

---

## 5-3. LangGraph vs CrewAI

### CrewAI
- 멀티 Agent 협업 구조에 친화적
- 역할 기반 Agent 팀 구성에 적합

### LangGraph
- 더 범용적
- 상태와 흐름을 더 세밀하게 제어 가능

### 쉽게 구분

- **CrewAI**: 여러 Agent가 역할 분담하는 팀 구조
- **LangGraph**: 흐름 엔진처럼 세밀하게 설계

---

## 6. 선택 기준

### LangChain을 선택하면 좋은 경우
- 빨리 만들어야 할 때
- RAG 챗봇
- Tool Calling 실험
- 간단한 Agent

### LangGraph를 선택하면 좋은 경우
- 조건 분기가 많을 때
- 상태 저장이 중요할 때
- 승인/검토 플로우가 있을 때
- Agent가 길게 실행되거나 재개가 필요할 때

### Step Functions를 선택하면 좋은 경우
- AWS 서비스 간 실행 순서를 설계할 때
- Lambda/ECS/DynamoDB/SNS 중심 시스템일 때

### Airflow를 선택하면 좋은 경우
- ETL
- 배치
- 정기 스케줄링
- 데이터 파이프라인

### CrewAI를 선택하면 좋은 경우
- 멀티 Agent 역할 협업이 핵심일 때

### 6-1. 이 저장소에서 바로 볼 수 있는 관련 클래스(차시)

- LangChain 차시: `class393 ~ class448` (`langChainLab/`)
- LangGraph 차시: 현재 별도 디렉터리형 차시는 없고, 이 문서 8~9절과 `tools/test_langchain_langgraph_practice.py`로 실습 가능

| 범위 | 주제 |
|---|---|
| class393~398 | LangChain 개요 |
| class399~404 | PromptTemplate |
| class405~409 | Model/LLM 연결 |
| class410~415 | OutputParser |
| class416~420 | Chain 구성 |
| class421~426 | Memory 활용 |
| class427~432 | Tool/Agent 기초 |
| class433~437 | 문서 로딩과 분할 |
| class438~443 | VectorStore 연동 |
| class444~448 | 실전 체인 애플리케이션 |

빠른 확인 명령:

```bash
source .venv/bin/activate
python langChainLab/class393/class393_example1.py
python langChainLab/class418/class418_example1.py
python langChainLab/class448/class448_example1.py
python tools/test_langchain_langgraph_practice.py
```

---

## 7. Python 최소 예제 - LangChain

아래는 외부 API 키 없이 로컬에서 바로 실행 가능한 최소 체인 예제입니다.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "너는 개념을 짧게 설명하는 튜터야."),
        ("human", "질문: {question}"),
    ]
)

def local_model(prompt_value):
    question_line = prompt_value.messages[-1].content
    return f"[LOCAL-DEMO] {question_line} -> 체인은 입력/처리/출력 단계를 연결합니다."

chain = prompt | RunnableLambda(local_model)
result = chain.invoke({"question": "LangChain 체인이 뭐야?"})

print(result)
```

### 이 예제의 의미

- `ChatPromptTemplate`: 프롬프트 템플릿 구성
- `RunnableLambda`: 실행 단위(노드) 연결
- `invoke(...)`: 입력 실행

### 해석

LangChain은 아래 같은 감각입니다.

```text
질문 -> Prompt -> Runnable -> 응답
```

실제 OpenAI 모델까지 붙이는 확장 실습을 하려면 `langchain-openai`와 API 키가 추가로 필요합니다.

---

## 8. Python 최소 예제 - LangGraph

아래는 가장 단순한 LangGraph 형태입니다.

```python
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {
        "messages": [
            {"role": "ai", "content": "hello world"}
        ]
    }

graph = StateGraph(MessagesState)

graph.add_node("mock_llm", mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)

app = graph.compile()

result = app.invoke(
    {
        "messages": [
            {"role": "user", "content": "안녕"}
        ]
    }
)

print(result)
```

### 이 예제의 의미

- `MessagesState`: 메시지 상태
- `add_node(...)`: 작업 단위 추가
- `add_edge(...)`: 실행 순서 연결
- `compile()`: 실행 가능한 앱 생성

### 해석

LangGraph는 아래 같은 감각입니다.

```text
START -> Node -> END
```

---

## 9. Python 최소 예제 - LangGraph 분기 처리

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class MyState(TypedDict):
    question: str
    route: str
    answer: str

def classify_node(state: MyState):
    q = state["question"]
    if "날씨" in q:
        return {"route": "weather"}
    return {"route": "general"}

def weather_node(state: MyState):
    return {"answer": "날씨 관련 처리 결과입니다."}

def general_node(state: MyState):
    return {"answer": "일반 질문 처리 결과입니다."}

def route_fn(state: MyState):
    return state["route"]

graph = StateGraph(MyState)

graph.add_node("classify", classify_node)
graph.add_node("weather", weather_node)
graph.add_node("general", general_node)

graph.add_edge(START, "classify")
graph.add_conditional_edges(
    "classify",
    route_fn,
    {
        "weather": "weather",
        "general": "general"
    }
)
graph.add_edge("weather", END)
graph.add_edge("general", END)

app = graph.compile()

result = app.invoke({"question": "서울 날씨 알려줘", "route": "", "answer": ""})
print(result)
```

### 이 예제의 핵심

- 먼저 질문을 분류
- 상태에 route 저장
- route에 따라 다음 노드 결정
- 마지막에 answer 생성

이것이 LangGraph의 핵심 감각입니다.

---

## 9-1. 실습 점검 스크립트

저장소에는 LangChain/LangGraph 실습을 한 번에 확인하는 smoke test 스크립트가 있습니다.

```bash
source .venv/bin/activate
python tools/test_langchain_langgraph_practice.py
```

- 검사 1: `langChainLab/class393~448`의 `example1` 실행
- 검사 2: LangChain 로컬 체인 예제 실행
- 검사 3: LangGraph 기본/분기 예제 실행

---

## 10. 학습 순서 추천

### 1단계
LangChain으로 시작
- Agent
- Tool
- Prompt
- Invoke

### 2단계
LangGraph로 확장
- State
- Node
- Edge
- Conditional Edge

### 3단계
실무형으로 발전
- Memory
- Persistence
- Human-in-the-loop
- Multi Agent
- 운영/관찰 체계

---

## 11. 실무 한 줄 요약

- **LangChain**: AI 앱을 빨리 만든다
- **LangGraph**: AI Agent의 상태와 흐름을 정교하게 제어한다
- **Step Functions**: AWS 서비스 실행 흐름을 제어한다
- **Airflow**: 배치/ETL/스케줄링에 강하다
- **CrewAI**: 멀티 Agent 협업 구조에 강하다

---

## 12. 최종 결론

처음에는 보통 **LangChain**으로 시작하는 것이 좋습니다.

이유:
- 빠르게 결과를 볼 수 있음
- RAG, Tool Calling, 챗봇을 쉽게 구현 가능

그 다음, 아래 요구사항이 생기면 **LangGraph**로 확장하는 것이 자연스럽습니다.

- 조건 분기
- 재시도
- 복구
- 승인 프로세스
- 장기 실행
- 멀티 Agent 협업

즉,

- 빠른 시작은 **LangChain**
- 복잡한 운영형 Agent는 **LangGraph**

이렇게 이해하면 가장 실무적입니다.
