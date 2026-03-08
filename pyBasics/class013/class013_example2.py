# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class013 example2: while 루프로 목표값 찾기"""

TOPIC = "반복문과 흐름제어"


def find_first_multiple(limit, base):
    n = 1
    while n <= limit:
        if n % base == 0:
            return n
        n += 1
    return -1


def main():
    print("오늘 주제:", TOPIC)
    print("1~30 중 7의 첫 배수:", find_first_multiple(30, 7))


if __name__ == "__main__":
    main()
