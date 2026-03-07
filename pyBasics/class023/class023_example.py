# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class023 example1: 컬렉션 자료구조"""

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


if __name__ == "__main__":
    main()
