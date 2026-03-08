# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class012 example3: 게임 보상 조건"""

TOPIC = "연산자와 조건문"


def reward(combo, has_ticket, hp):
    if combo >= 50 and has_ticket and hp > 0:
        return "전설 상자"
    if combo >= 20 or has_ticket:
        return "희귀 상자"
    return "일반 상자"


def main():
    print("오늘 주제:", TOPIC)
    print("플레이어 A:", reward(55, True, 10))
    print("플레이어 B:", reward(12, True, 5))


if __name__ == "__main__":
    main()
