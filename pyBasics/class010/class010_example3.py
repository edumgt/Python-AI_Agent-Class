# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class010 example3: 비밀번호 조건 검사"""

TOPIC = "연산자와 조건문"


def password_check(password):
    long_enough = len(password) >= 8
    has_digit = any(ch.isdigit() for ch in password)
    has_symbol = "!" in password or "@" in password or "#" in password
    return long_enough and has_digit and has_symbol


def main():
    password = "study2026!"
    print("오늘 주제:", TOPIC)
    print(f"비밀번호 '{password}' 사용 가능 여부: {password_check(password)}")


if __name__ == "__main__":
    main()
