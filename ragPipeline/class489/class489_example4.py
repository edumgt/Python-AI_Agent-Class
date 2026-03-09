# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class489 example4: 응답 검증/출처화 · 단계 4/5 실전 검증 [class489]"""

TOPIC = "응답 검증/출처화 · 단계 4/5 실전 검증 [class489]"
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

def mini_project_plan():
    return {
        "scenario": "검색 점수 임계치 기반 필터를 적용해 응답 품질을 높이세요.",
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
