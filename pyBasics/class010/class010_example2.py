# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class010 example2: 연산자와 조건문 · 단계 2/4 기초 구현 [class010]"""

TOPIC = "연산자와 조건문 · 단계 2/4 기초 구현 [class010]"
EXAMPLE_TEMPLATE = "condition"

def route_incident(score):
    if score >= 90:
        return "critical"
    if score >= 70:
        return "warning"
    if score >= 50:
        return "observe"
    return "ok"

def main():
    print("오늘 주제:", TOPIC)
    sample_scores = [35, 58, 77, 94]
    routed = {score: route_incident(score) for score in sample_scores}
    print("라우팅:", routed)
    return {"max_level": route_incident(max(sample_scores)), "count": len(sample_scores)}

def extension_mission():
    return {
        "mission": "입력값 2세트를 비교하고 차이를 기록하세요.",
        "check": "예외 케이스 1개를 추가해 방어 로직을 검증하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
