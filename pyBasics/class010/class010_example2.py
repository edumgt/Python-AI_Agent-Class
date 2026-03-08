# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class010 example2: 나이/요일 조건으로 영화요금 계산"""

TOPIC = "연산자와 조건문"


def movie_price(age, is_weekend):
    base = 12000 if is_weekend else 10000
    if age <= 12:
        return int(base * 0.5)
    if age >= 65:
        return int(base * 0.7)
    return base


def main():
    fee = movie_price(age=11, is_weekend=True)
    print("오늘 주제:", TOPIC)
    print(f"주말 어린이 요금: {fee}원")


if __name__ == "__main__":
    main()
