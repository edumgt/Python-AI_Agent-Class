# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class424 example1: Memory 활용 · 단계 4/6 응용 확장 [class424]"""

TOPIC = "Memory 활용 · 단계 4/6 응용 확장 [class424]"
EXAMPLE_TEMPLATE = "langchain"

def step_collect(question):
    return {"question": question, "context": []}

def step_retrieve(state):
    state["context"] = [
        "체인은 여러 단계를 연결한다",
        "도구 호출 전 입력 검증이 중요하다",
    ]
    return state

def step_answer(state):
    context = " / ".join(state["context"])
    return {"answer": f"질문: {state['question']} | 근거: {context}", "steps": 3}

def main():
    print("오늘 주제:", TOPIC)
    s1 = step_collect("체인 설계의 핵심이 뭐야?")
    s2 = step_retrieve(s1)
    report = step_answer(s2)
    print("체인 실행 결과:", report)
    return report

if __name__ == "__main__":
    main()
