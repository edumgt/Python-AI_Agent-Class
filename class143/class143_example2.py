# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class143 example2: 텍스트 데이터 수집"""

TOPIC = "텍스트 데이터 수집"
EXAMPLE_TEMPLATE = "nlp"

def tokenize(text):
    cleaned = text.replace(",", " ").replace(".", " ")
    return [tok.lower() for tok in cleaned.split() if tok]

def top_words(tokens):
    freq = {}
    for tok in tokens:
        freq[tok] = freq.get(tok, 0) + 1
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)

def main():
    print("오늘 주제:", TOPIC)
    tokens = tokenize("AI 수업은 재미있고, AI 실습은 유익하다.")
    print("토큰:", tokens)
    print("빈도:", top_words(tokens))


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
