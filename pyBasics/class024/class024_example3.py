# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class024 example3: 컬렉션 자료구조 · 단계 4/4 운영 최적화 [class024]"""

TOPIC = "컬렉션 자료구조 · 단계 4/4 운영 최적화 [class024]"
EXAMPLE_TEMPLATE = "collection"

def summarize_orders(orders):
    by_team = {}
    for row in orders:
        by_team[row["team"]] = by_team.get(row["team"], 0) + row["amount"]
    ranking = sorted(by_team.items(), key=lambda x: x[1], reverse=True)
    return by_team, ranking

def main():
    print("오늘 주제:", TOPIC)
    orders = [
        {"team": "A", "amount": 120},
        {"team": "B", "amount": 90},
        {"team": "A", "amount": 60},
        {"team": "C", "amount": 200},
    ]
    by_team, ranking = summarize_orders(orders)
    print("팀별 합계:", by_team)
    print("랭킹:", ranking)
    return {"winner": ranking[0][0], "team_count": len(by_team)}

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
