# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class013 example1: for + continue로 짝수만 누적"""

TOPIC = "반복문과 흐름제어"


def sum_even(numbers):
    total = 0
    for n in numbers:
        if n % 2 != 0:
            continue
        total += n
    return total


def main():
    nums = [3, 4, 5, 6, 8, 11]
    print("오늘 주제:", TOPIC)
    print(f"짝수 합: {sum_even(nums)}")


if __name__ == "__main__":
    main()
