# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class341 example3: API 연동 실습 · 단계 1/6 입문 이해 [class341]"""

TOPIC = "API 연동 실습 · 단계 1/6 입문 이해 [class341]"
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

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "핵심 함수를 재사용 가능한 모듈로 분리하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
