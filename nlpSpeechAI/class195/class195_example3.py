# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class195 example3: 텍스트 분류 기초"""

TOPIC = "텍스트 분류 기초"
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
