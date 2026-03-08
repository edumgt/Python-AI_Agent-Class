# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
"""class013 example3: break로 검색 조기 종료"""

TOPIC = "반복문과 흐름제어"


def find_name(names, target):
    for idx, name in enumerate(names):
        if name == target:
            return idx
    return -1


def main():
    roster = ["mina", "jisu", "taeho", "yuna"]
    print("오늘 주제:", TOPIC)
    print("yuna 위치:", find_name(roster, "yuna"))


if __name__ == "__main__":
    main()
