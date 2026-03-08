# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class009 example2: 연산자 우선순위와 괄호 비교"""

TOPIC = "연산자와 조건문"


def can_join_event(age, is_member, has_coupon):
    without_parentheses = age >= 14 and is_member or has_coupon
    with_parentheses = age >= 14 and (is_member or has_coupon)
    return without_parentheses, with_parentheses


def main():
    age = 12
    is_member = False
    has_coupon = True
    a, b = can_join_event(age, is_member, has_coupon)
    print("오늘 주제:", TOPIC)
    print(f"괄호 없음 결과: {a}")
    print(f"괄호 사용 결과: {b}")


if __name__ == "__main__":
    main()
