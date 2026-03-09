# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
from typing import TypedDict


ROOT = Path(__file__).resolve().parents[1]
PYTHON_BIN = ROOT / ".venv" / "bin" / "python"
if not PYTHON_BIN.exists():
    PYTHON_BIN = Path(sys.executable)


def run_python_file(path: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [str(PYTHON_BIN), str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    merged = (proc.stdout + proc.stderr).strip()
    tail = "\n".join(merged.splitlines()[-5:]) if merged else ""
    return proc.returncode == 0, tail


def smoke_langchain_examples() -> tuple[int, list[str]]:
    failures: list[str] = []
    checked = 0
    for n in range(393, 449):
        class_id = f"class{n}"
        path = ROOT / "langChainLab" / class_id / f"{class_id}_example1.py"
        checked += 1
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT)}: missing")
            continue

        ok, tail = run_python_file(path)
        if not ok:
            failures.append(f"{path.relative_to(ROOT)}: runtime error\n{tail}")

    return checked, failures


def smoke_local_langchain() -> str:
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
    if "체인은 입력/처리/출력" not in result:
        raise AssertionError(f"unexpected result: {result}")
    return result


def smoke_local_langgraph_basic() -> dict:
    from langgraph.graph import END, START, MessagesState, StateGraph

    def mock_llm(state: MessagesState):
        return {"messages": [{"role": "ai", "content": "hello world"}]}

    graph = StateGraph(MessagesState)
    graph.add_node("mock_llm", mock_llm)
    graph.add_edge(START, "mock_llm")
    graph.add_edge("mock_llm", END)
    app = graph.compile()

    result = app.invoke({"messages": [{"role": "user", "content": "안녕"}]})
    if "messages" not in result or len(result["messages"]) < 2:
        raise AssertionError(f"unexpected result: {result}")
    return result


class RouteState(TypedDict):
    question: str
    route: str
    answer: str


def smoke_local_langgraph_branch() -> RouteState:
    from langgraph.graph import END, START, StateGraph

    def classify_node(state: RouteState):
        q = state["question"]
        if "날씨" in q:
            return {"route": "weather"}
        return {"route": "general"}

    def weather_node(_: RouteState):
        return {"answer": "날씨 관련 처리 결과입니다."}

    def general_node(_: RouteState):
        return {"answer": "일반 질문 처리 결과입니다."}

    def route_fn(state: RouteState):
        return state["route"]

    graph = StateGraph(RouteState)
    graph.add_node("classify", classify_node)
    graph.add_node("weather", weather_node)
    graph.add_node("general", general_node)
    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify",
        route_fn,
        {"weather": "weather", "general": "general"},
    )
    graph.add_edge("weather", END)
    graph.add_edge("general", END)
    app = graph.compile()

    result = app.invoke({"question": "서울 날씨 알려줘", "route": "", "answer": ""})
    if result.get("route") != "weather":
        raise AssertionError(f"unexpected route: {result}")
    if not result.get("answer"):
        raise AssertionError(f"answer missing: {result}")
    return result


def main() -> int:
    print(f"python={PYTHON_BIN}")

    checked, failures = smoke_langchain_examples()
    print(f"[langChainLab example1] checked={checked} failed={len(failures)}")
    for msg in failures[:20]:
        print(f"- {msg}")

    extras_failed = 0
    try:
        lc_result = smoke_local_langchain()
        print(f"[langchain local] OK: {lc_result}")
    except Exception as exc:
        extras_failed += 1
        print(f"[langchain local] FAIL: {type(exc).__name__}: {exc}")

    try:
        lg_basic = smoke_local_langgraph_basic()
        print(f"[langgraph basic] OK: messages={len(lg_basic.get('messages', []))}")
    except Exception as exc:
        extras_failed += 1
        print(f"[langgraph basic] FAIL: {type(exc).__name__}: {exc}")

    try:
        lg_branch = smoke_local_langgraph_branch()
        print(
            f"[langgraph branch] OK: route={lg_branch.get('route')} answer={lg_branch.get('answer')}"
        )
    except Exception as exc:
        extras_failed += 1
        print(f"[langgraph branch] FAIL: {type(exc).__name__}: {exc}")

    total_failures = len(failures) + extras_failed
    print(f"total_failures={total_failures}")
    return 1 if total_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
