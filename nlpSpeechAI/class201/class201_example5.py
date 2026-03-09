# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class201 example5: 시퀀스 모델 기초 · 단계 1/8 입문 이해 [class201]"""

TOPIC = "시퀀스 모델 기초 · 단계 1/8 입문 이해 [class201]"
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

def ops_readiness_check():
    return {
        "risk": "운영 체크리스트(모니터링/알림/복구)를 정의하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
