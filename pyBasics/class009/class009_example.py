# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class009 example1: 비교/논리 연산자로 합격 판정하기"""

TOPIC = "연산자와 조건문"


def check_pass(score, attendance):
    passed_score = score >= 70
    passed_attendance = attendance >= 80
    return passed_score and passed_attendance


def main():
    score = 78
    attendance = 85
    result = check_pass(score, attendance)
    print("오늘 주제:", TOPIC)
    print(f"점수={score}, 출석={attendance}% -> 합격 여부: {result}")


if __name__ == "__main__":
    main()
