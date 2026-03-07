# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class012 example2: 연산자와 조건문"""

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


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
