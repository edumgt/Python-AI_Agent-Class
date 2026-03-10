# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class024 example1: 컬렉션 자료구조 · 단계 4/4 운영 최적화 [class024]"""

TOPIC = "컬렉션 자료구조 · 단계 4/4 운영 최적화 [class024]"
EXAMPLE_TEMPLATE = "collection"
EXAMPLE_VARIANT = 1

def summarize_orders(orders):
    teams_list = [row["team"] for row in orders]
    unique_teams_set = set(teams_list)
    top_slice = teams_list[: min(3, len(teams_list))]
    by_team_dict = {}
    for row in orders:
        by_team_dict[row["team"]] = by_team_dict.get(row["team"], 0) + row["amount"]
    ranking_tuple = tuple(sorted(by_team_dict.items(), key=lambda x: x[1], reverse=True))
    high_orders = [row for row in orders if row["amount"] >= 100]
    return {
        "team_list": teams_list,
        "unique_teams": unique_teams_set,
        "top_slice": top_slice,
        "by_team": by_team_dict,
        "ranking": ranking_tuple,
        "high_orders": high_orders,
    }

def choose_structure(use_case):
    if use_case == "ordered":
        return "list"
    if use_case == "immutable":
        return "tuple"
    if use_case == "lookup":
        return "dict"
    return "set"

def build_test_cases():
    cases = [
        (
            "baseline",
            [
                {"team": "A", "amount": 120},
                {"team": "B", "amount": 90},
                {"team": "A", "amount": 60},
                {"team": "C", "amount": 200},
            ],
        )
    ]
    if EXAMPLE_VARIANT >= 2:
        cases.append(
            (
                "with_duplicate",
                [
                    {"team": "A", "amount": 10},
                    {"team": "A", "amount": 15},
                    {"team": "B", "amount": 40},
                ],
            )
        )
    if EXAMPLE_VARIANT >= 3:
        cases.append(
            (
                "many_teams",
                [
                    {"team": "D", "amount": 130},
                    {"team": "E", "amount": 70},
                    {"team": "F", "amount": 95},
                    {"team": "G", "amount": 160},
                ],
            )
        )
    if EXAMPLE_VARIANT >= 4:
        cases.append(
            (
                "small_values",
                [
                    {"team": "X", "amount": 8},
                    {"team": "Y", "amount": 12},
                    {"team": "Z", "amount": 18},
                ],
            )
        )
    if EXAMPLE_VARIANT >= 5:
        cases.append(
            (
                "mixed_values",
                [
                    {"team": "A", "amount": 300},
                    {"team": "B", "amount": 110},
                    {"team": "C", "amount": 75},
                    {"team": "B", "amount": 25},
                ],
            )
        )
    return cases

def main():
    print("오늘 주제:", TOPIC)
    reports = []
    for case_name, orders in build_test_cases():
        stats = summarize_orders(orders)
        structure = choose_structure("lookup" if len(stats["by_team"]) >= 3 else "ordered")
        report = {
            "case": case_name,
            "team_count": len(stats["unique_teams"]),
            "winner": stats["ranking"][0][0],
            "selected_structure": structure,
            "top_slice": stats["top_slice"],
            "high_order_count": len(stats["high_orders"]),
        }
        reports.append(report)
        print(f"[{case_name}] 컬렉션 리포트:", report)
    return {"variant": EXAMPLE_VARIANT, "case_count": len(reports)}

if __name__ == "__main__":
    main()
