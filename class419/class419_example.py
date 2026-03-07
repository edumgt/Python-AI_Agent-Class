# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class419 example1: Chain 구성"""

TOPIC = "Chain 구성"
EXAMPLE_TEMPLATE = "langchain"

def step_collect(question):
    return {"question": question}

def step_plan(state):
    return {"question": state["question"], "plan": "핵심 개념 3개로 설명"}

def step_answer(state):
    return f"[응답] {state['question']} -> {state['plan']}"

def main():
    print("오늘 주제:", TOPIC)
    s1 = step_collect("RAG가 뭐야?")
    s2 = step_plan(s1)
    print(step_answer(s2))


if __name__ == "__main__":
    main()
