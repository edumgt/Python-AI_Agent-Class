# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class419 쉬운 예제: Chain 구성"""

TOPIC = "Chain 구성"

def step_collect(question):
    return f"[수집] 질문 받음: {question}"

def step_summarize(text):
    return f"[요약] 핵심: {text[-10:]}"

def step_answer(summary):
    return f"[응답] {summary} 를 바탕으로 답변 생성"

def main():
    question = "지구가 태양 주위를 도는 이유를 알려줘"
    collected = step_collect(question)
    summary = step_summarize(collected)
    answer = step_answer(summary)
    print("오늘 주제:", TOPIC)
    print(collected)
    print(summary)
    print(answer)

if __name__ == "__main__":
    main()
