# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class012 example1: 성적 구간 판정"""

TOPIC = "연산자와 조건문"


def level_from_score(score):
    if score >= 95:
        return "S"
    if score >= 85:
        return "A"
    if score >= 75:
        return "B"
    return "C"


def main():
    score = 88
    print("오늘 주제:", TOPIC)
    print(f"점수 {score} -> 레벨 {level_from_score(score)}")


if __name__ == "__main__":
    main()
