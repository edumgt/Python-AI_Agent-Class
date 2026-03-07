# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class011 example1: 연산자와 조건문"""

TOPIC = "연산자와 조건문"
EXAMPLE_TEMPLATE = "condition"

def grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "D"

def main():
    score = 86
    print("오늘 주제:", TOPIC)
    print(f"점수 {score} -> 등급 {grade(score)}")


if __name__ == "__main__":
    main()
