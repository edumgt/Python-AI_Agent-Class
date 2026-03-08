# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class011 example2: 포인트/등급 조건으로 쿠폰 발급"""

TOPIC = "연산자와 조건문"


def issue_coupon(points, tier):
    if points >= 1000 and tier in ("gold", "vip"):
        return "20% 쿠폰"
    if points >= 500 or tier == "vip":
        return "10% 쿠폰"
    return "쿠폰 없음"


def main():
    print("오늘 주제:", TOPIC)
    print("고객1:", issue_coupon(1200, "gold"))
    print("고객2:", issue_coupon(450, "vip"))


if __name__ == "__main__":
    main()
