# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class318 example1: 요약/분류/추출 · 단계 4/6 응용 확장 [class318]"""

TOPIC = "요약/분류/추출 · 단계 4/6 응용 확장 [class318]"
EXAMPLE_TEMPLATE = "nlp"

def tokenize(text):
    cleaned = text.replace(",", " ").replace(".", " ").replace("/", " ")
    return [tok.lower() for tok in cleaned.split() if tok]

def top_k(tokens, k=5):
    freq = {}
    for tok in tokens:
        freq[tok] = freq.get(tok, 0) + 1
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:k]

def main():
    print("오늘 주제:", TOPIC)
    text = "LLM 응답 품질은 프롬프트 구조와 검증 절차에 따라 달라진다. 응답 품질을 점검하자."
    tokens = tokenize(text)
    ranking = top_k(tokens)
    report = {"token_count": len(tokens), "top_terms": ranking}
    print("분석 리포트:", report)
    return report

if __name__ == "__main__":
    main()
