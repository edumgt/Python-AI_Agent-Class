# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class017 example1: 함수와 모듈 · 단계 1/4 입문 이해 [class017]"""

TOPIC = "함수와 모듈 · 단계 1/4 입문 이해 [class017]"
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

if __name__ == "__main__":
    main()
