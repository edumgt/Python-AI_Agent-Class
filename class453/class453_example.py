# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class453 example1: RAG 개요"""

TOPIC = "RAG 개요"
EXAMPLE_TEMPLATE = "rag"

def retrieve(question, docs):
    q = set(question.split())
    scored = []
    for doc in docs:
        overlap = len(q & set(doc["text"].split()))
        scored.append((overlap, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored if score > 0][:2]

def answer(question, docs):
    if not docs:
        return "관련 문서를 찾지 못했어요."
    joined = " / ".join(d["text"] for d in docs)
    return f"질문: {question}\n근거: {joined}"

def main():
    docs = [
        {"id": 1, "text": "RAG는 검색 결과를 근거로 답변한다"},
        {"id": 2, "text": "벡터 검색으로 관련 문서를 찾는다"},
        {"id": 3, "text": "프롬프트 설계도 중요하다"},
    ]
    q = "RAG 답변 근거"
    picked = retrieve(q, docs)
    print("오늘 주제:", TOPIC)
    print("선택 문서:", [d["id"] for d in picked])
    print(answer(q, picked))


if __name__ == "__main__":
    main()
