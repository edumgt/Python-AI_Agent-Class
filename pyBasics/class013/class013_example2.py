# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class013 example2: 반복문과 흐름제어"""

TOPIC = "반복문과 흐름제어"
EXAMPLE_TEMPLATE = "loop"

def even_sum(limit):
    total = 0
    for n in range(1, limit + 1):
        if n % 2 == 0:
            total += n
    return total

def main():
    print("오늘 주제:", TOPIC)
    print("1~10 짝수 합:", even_sum(10))


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
