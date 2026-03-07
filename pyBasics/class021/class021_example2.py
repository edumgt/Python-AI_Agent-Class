# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class021 example2: 컬렉션 자료구조"""

TOPIC = "컬렉션 자료구조"
EXAMPLE_TEMPLATE = "collection"

def summarize_scores(scores):
    return {
        "count": len(scores),
        "max": max(scores),
        "min": min(scores),
        "avg": round(sum(scores) / len(scores), 2),
    }

def main():
    scores = [75, 88, 92, 81]
    print("오늘 주제:", TOPIC)
    print("요약:", summarize_scores(scores))


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
