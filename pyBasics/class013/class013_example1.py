# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class013 example1: 반복문과 흐름제어 · 단계 1/4 입문 이해 [class013]"""

TOPIC = "반복문과 흐름제어 · 단계 1/4 입문 이해 [class013]"
EXAMPLE_TEMPLATE = "loop"
EXAMPLE_VARIANT = 1

def rolling_average(values, window):
    result = []
    for idx in range(len(values)):
        start = max(0, idx - window + 1)
        chunk = values[start : idx + 1]
        result.append(round(sum(chunk) / len(chunk), 2))
    return result

def bounded_scan(values, stop_at):
    accepted = []
    idx = 0
    while idx < len(values):
        current = values[idx]
        idx += 1
        if current < 0:
            continue
        if current >= stop_at:
            break
        accepted.append(current)
    return accepted

def multiplication_grid(size):
    grid = []
    for i in range(1, size + 1):
        row = []
        for j in range(1, size + 1):
            row.append(i * j)
        grid.append(row)
    return grid

def build_test_cases():
    cases = [("baseline", [12, 15, 13, 20, 19, 23])]
    if EXAMPLE_VARIANT >= 2:
        cases.append(("with_zero", [5, 0, 7, 9, 0, 11]))
    if EXAMPLE_VARIANT >= 3:
        cases.append(("with_negative", [8, -1, 6, 4, -3, 9]))
    if EXAMPLE_VARIANT >= 4:
        cases.append(("longer_seq", [3, 6, 9, 12, 15, 18, 21, 24]))
    if EXAMPLE_VARIANT >= 5:
        cases.append(("high_values", [25, 33, 41, 58, 72, 91]))
    return cases

def main():
    print("오늘 주제:", TOPIC)
    reports = []
    for case_name, values in build_test_cases():
        trend = rolling_average(values, window=3)
        accepted = bounded_scan(values, stop_at=50)
        grid = multiplication_grid(2 + min(EXAMPLE_VARIANT, 3))
        report = {
            "case": case_name,
            "points": len(values),
            "last_avg": trend[-1],
            "accepted_count": len(accepted),
            "grid_last": grid[-1][-1],
        }
        reports.append(report)
        print(f"[{case_name}] 리포트:", report)
    return {"variant": EXAMPLE_VARIANT, "case_count": len(reports), "reports": reports}

if __name__ == "__main__":
    main()
