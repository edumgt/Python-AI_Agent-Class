# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class419 example3: Chain 구성 · 단계 4/5 실전 검증 [class419]"""

TOPIC = "Chain 구성 · 단계 4/5 실전 검증 [class419]"
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

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "도구 호출 실패를 예외 처리해 회복 가능한 체인을 만드세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
