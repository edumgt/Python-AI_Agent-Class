# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class009 example3: 조건문으로 할인율 결정"""

TOPIC = "연산자와 조건문"


def discount_rate(total_price):
    if total_price >= 100000:
        return 0.2
    if total_price >= 50000:
        return 0.1
    return 0.0


def main():
    total_price = 67000
    rate = discount_rate(total_price)
    final_price = int(total_price * (1 - rate))
    print("오늘 주제:", TOPIC)
    print(f"원가={total_price}원, 할인율={int(rate * 100)}%, 결제금액={final_price}원")


if __name__ == "__main__":
    main()
