# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class147 example2: 텍스트 정제와 토큰화 · 단계 3/8 기초 구현 [class147]"""

TOPIC = "텍스트 정제와 토큰화 · 단계 3/8 기초 구현 [class147]"
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

def extension_mission():
    return {
        "mission": "입력값 2세트를 비교하고 차이를 기록하세요.",
        "check": "예외 케이스 1개를 추가해 방어 로직을 검증하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
