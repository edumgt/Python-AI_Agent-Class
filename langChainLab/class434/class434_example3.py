# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class434 example3: 문서 로딩과 분할 · 단계 2/5 기초 구현 [class434]"""

TOPIC = "문서 로딩과 분할 · 단계 2/5 기초 구현 [class434]"
EXAMPLE_TEMPLATE = "rag"
EXAMPLE_VARIANT = 3

def tokenize(text):
    return [t.lower() for t in text.replace(",", " ").replace(".", " ").split() if t]

def retrieve(question, docs, top_k=2):
    q = set(tokenize(question))
    scored = []
    for doc in docs:
        overlap = len(q & set(tokenize(doc["text"])))
        if overlap > 0:
            scored.append({"id": doc["id"], "text": doc["text"], "score": overlap})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]

def answer(question, hits):
    if not hits:
        return {"answer": "관련 문서를 찾지 못했습니다.", "citations": []}
    citations = [f"doc{h['id']}" for h in hits]
    evidence = " | ".join(h["text"] for h in hits)
    return {"answer": f"질문: {question} -> {evidence}", "citations": citations}

def main():
    print("오늘 주제:", TOPIC)
    docs = [
        {"id": 1, "text": "RAG는 검색 결과를 근거로 답한다"},
        {"id": 2, "text": "벡터 인덱스는 유사도 검색 속도를 높인다"},
        {"id": 3, "text": "프롬프트 템플릿은 출력 형식을 고정한다"},
    ]
    question = "RAG 답변 근거를 어떻게 확보하나요"
    hits = retrieve(question, docs)
    report = answer(question, hits)
    print("검색 히트:", [h["id"] for h in hits])
    print("응답:", report)
    return report

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "질문 재작성(query rewrite) 전/후 검색 결과를 비교하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
