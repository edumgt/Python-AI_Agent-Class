# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class020 example2: 함수와 모듈 · 단계 4/4 운영 최적화 [class020]"""

TOPIC = "함수와 모듈 · 단계 4/4 운영 최적화 [class020]"
EXAMPLE_TEMPLATE = "function_module"

import math

def area_circle(radius):
    return round(math.pi * radius * radius, 3)

def perimeter_rectangle(width, height):
    return 2 * (width + height)

def main():
    print("오늘 주제:", TOPIC)
    c_area = area_circle(3)
    r_perimeter = perimeter_rectangle(4, 7)
    print("원 넓이:", c_area)
    print("직사각형 둘레:", r_perimeter)
    return {"circle_area": c_area, "rect_perimeter": r_perimeter}

def extension_mission():
    return {
        "mission": "입력값 2세트를 비교하고 차이를 기록하세요.",
        "check": "예외 케이스 1개를 추가해 방어 로직을 검증하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
