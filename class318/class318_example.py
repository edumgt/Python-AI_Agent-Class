# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class318 쉬운 예제: 요약/분류/추출"""

TOPIC = "요약/분류/추출"

def tokenize(sentence):
    cleaned = sentence.replace(",", " ").replace(".", " ")
    return [token.lower() for token in cleaned.split() if token]

def word_count(tokens):
    counts = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return counts

def main():
    sentence = "AI 수업은 재미있고, AI 실습은 더 재미있다."
    tokens = tokenize(sentence)
    counts = word_count(tokens)
    print("오늘 주제:", TOPIC)
    print("토큰:", tokens)
    print("빈도:", counts)

if __name__ == "__main__":
    main()
