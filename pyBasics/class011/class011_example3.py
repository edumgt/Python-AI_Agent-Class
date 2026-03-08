# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class011 example3: 과속 벌점 조건 분기"""

TOPIC = "연산자와 조건문"


def speed_penalty(speed, in_school_zone):
    limit = 30 if in_school_zone else 60
    over = speed - limit
    if over <= 0:
        return "정상 주행"
    if over <= 20:
        return "벌점 10점"
    return "벌점 30점"


def main():
    print("오늘 주제:", TOPIC)
    print("학교 앞 42km/h:", speed_penalty(42, True))
    print("일반도로 95km/h:", speed_penalty(95, False))


if __name__ == "__main__":
    main()
