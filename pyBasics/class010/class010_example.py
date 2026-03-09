# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class010 example1: 연산자와 조건문 · 단계 2/4 기초 구현 [class010]"""

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

if __name__ == "__main__":
    main()
