# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class012 example3: 연산자와 조건문 · 단계 4/4 운영 최적화 [class012]"""

TOPIC = "연산자와 조건문 · 단계 4/4 운영 최적화 [class012]"
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

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "핵심 함수를 재사용 가능한 모듈로 분리하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
