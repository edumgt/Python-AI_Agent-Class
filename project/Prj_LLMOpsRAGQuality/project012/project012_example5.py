# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""project012 example5: LLMOps/RAG 서비스 품질관리 · 단계 2/5 기초 구현 [project012]"""

TOPIC = "LLMOps/RAG 서비스 품질관리 · 단계 2/5 기초 구현 [project012]"
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

def ops_readiness_check():
    return {
        "risk": "인덱스 갱신 주기와 실패 시 재시도 정책을 정하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
