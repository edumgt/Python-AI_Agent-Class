# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class482 쉬운 예제: 프롬프트 결합"""

TOPIC = "프롬프트 결합"

def retrieve(question, docs):
    q_tokens = set(question.split())
    scored = []
    for doc in docs:
        d_tokens = set(doc["text"].split())
        score = len(q_tokens & d_tokens)
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored if score > 0][:2]

def build_answer(question, picked_docs):
    if not picked_docs:
        return "관련 문서를 찾지 못했어요."
    evidence = " / ".join(doc["text"] for doc in picked_docs)
    return f"질문: {question}\n근거: {evidence}"

def main():
    docs = [
        {"id": 1, "text": "지구는 태양 주위를 1년에 한 번 공전한다"},
        {"id": 2, "text": "달은 지구 주위를 약 27일에 한 번 돈다"},
        {"id": 3, "text": "태양은 태양계의 중심 별이다"},
    ]
    question = "지구와 태양의 관계를 알려줘"
    picked = retrieve(question, docs)
    answer = build_answer(question, picked)
    print("오늘 주제:", TOPIC)
    print("검색 문서 id:", [doc["id"] for doc in picked])
    print(answer)

if __name__ == "__main__":
    main()
