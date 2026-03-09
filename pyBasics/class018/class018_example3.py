# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class018 example3: 함수와 모듈 · 단계 2/4 기초 구현 [class018]"""

TOPIC = "함수와 모듈 · 단계 2/4 기초 구현 [class018]"
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

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "핵심 함수를 재사용 가능한 모듈로 분리하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
