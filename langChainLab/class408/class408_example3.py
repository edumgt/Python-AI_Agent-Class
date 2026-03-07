# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class408 example3: Model/LLM 연결"""

TOPIC = "Model/LLM 연결"
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


def self_check():
    return [
        "입력/출력 형식을 다시 설명할 수 있는가?",
        "오류 상황 1가지를 직접 만들어 테스트했는가?",
        "핵심 로직을 함수 단위로 분리했는가?",
    ]

def challenge_case():
    return {
        "task": "같은 로직을 새로운 입력 데이터로 재실행",
        "goal": "결과 차이를 한 문장으로 요약",
    }

if __name__ == "__main__":
    main()
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
