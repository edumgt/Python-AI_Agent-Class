# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class011 example1: 단락 평가로 0 나누기 방지"""

TOPIC = "연산자와 조건문"


def safe_division(a, b):
    return b != 0 and (a / b) > 1


def main():
    print("오늘 주제:", TOPIC)
    print("10 / 2 검사:", safe_division(10, 2))
    print("10 / 0 검사:", safe_division(10, 0))


if __name__ == "__main__":
    main()
