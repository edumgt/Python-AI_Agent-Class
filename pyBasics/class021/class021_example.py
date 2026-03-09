# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class021 example1: 컬렉션 자료구조 · 단계 1/4 입문 이해 [class021]"""

TOPIC = "컬렉션 자료구조 · 단계 1/4 입문 이해 [class021]"
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

if __name__ == "__main__":
    main()
