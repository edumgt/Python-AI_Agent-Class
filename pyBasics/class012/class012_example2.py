# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class012 example2: 주문 상태 결정"""

TOPIC = "연산자와 조건문"


def order_status(is_paid, in_stock, same_day):
    if not is_paid:
        return "결제 대기"
    if is_paid and not in_stock:
        return "재고 대기"
    if same_day:
        return "당일 출고"
    return "일반 출고"


def main():
    print("오늘 주제:", TOPIC)
    print("주문1:", order_status(True, True, True))
    print("주문2:", order_status(True, False, False))


if __name__ == "__main__":
    main()
