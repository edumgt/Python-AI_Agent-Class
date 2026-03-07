# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class032 example3: 예외처리와 디버깅"""

TOPIC = "예외처리와 디버깅"
EXAMPLE_TEMPLATE = "exception"

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "0으로 나눌 수 없어요."

def main():
    print("오늘 주제:", TOPIC)
    print("10 / 2 =", safe_divide(10, 2))
    print("10 / 0 =", safe_divide(10, 0))


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
