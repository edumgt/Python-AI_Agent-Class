# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class445 example4: 실전 체인 애플리케이션 · 단계 2/5 기초 구현 [class445]"""

TOPIC = "실전 체인 애플리케이션 · 단계 2/5 기초 구현 [class445]"
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

def mini_project_plan():
    return {
        "scenario": "state 객체에 trace_id를 넣고 단계별 추적 기능을 추가하세요.",
        "steps": [
            "1) baseline 실행",
            "2) 개선안 적용",
            "3) 지표/로그 비교",
        ],
        "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("미니 프로젝트:", mini_project_plan())
