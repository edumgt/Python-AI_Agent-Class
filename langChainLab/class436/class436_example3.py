# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class436 example3: 문서 로딩과 분할"""

TOPIC = "문서 로딩과 분할"
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
