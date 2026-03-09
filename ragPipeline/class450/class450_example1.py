# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class450 example1: RAG 개요 · 단계 2/6 기초 구현 [class450]"""

TOPIC = "RAG 개요 · 단계 2/6 기초 구현 [class450]"
EXAMPLE_TEMPLATE = "rag"

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

if __name__ == "__main__":
    main()
