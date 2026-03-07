# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class019 example2: 함수와 모듈"""

TOPIC = "함수와 모듈"
EXAMPLE_TEMPLATE = "function_module"

import math

def area_circle(radius):
    return round(math.pi * radius * radius, 2)

def main():
    r = 3
    print("오늘 주제:", TOPIC)
    print(f"반지름 {r} 원의 넓이:", area_circle(r))


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
