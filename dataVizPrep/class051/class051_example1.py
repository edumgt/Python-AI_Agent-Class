# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class051 example1: Pandas 데이터프레임 기초 · 단계 3/4 실전 검증 [class051]"""

TOPIC = "Pandas 데이터프레임 기초 · 단계 3/4 실전 검증 [class051]"
EXAMPLE_TEMPLATE = "pandas"
EXAMPLE_VARIANT = 1

try:
    import pandas as pd
except ImportError:
    pd = None

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def normalize_rows(rows):
    cleaned = []
    dropped = []
    for idx, row in enumerate(rows, start=1):
        score = safe_float(row.get("score"))
        name = str(row.get("name", "")).strip() or f"unknown-{idx}"
        if score is None:
            dropped.append({"row": idx, "reason": "invalid_score", "raw": row.get("score")})
            continue
        cleaned.append({"name": name, "score": score})
    return cleaned, dropped

def summarize_scores(rows):
    cleaned, dropped = normalize_rows(rows)
    if not cleaned:
        return {"backend": "python", "avg": 0.0, "pass_count": 0, "row_count": 0, "dropped_count": len(dropped)}

    if pd is None:
        avg = sum(r["score"] for r in cleaned) / len(cleaned)
        passed = sum(1 for r in cleaned if r["score"] >= 80)
        return {
            "backend": "python",
            "avg": round(avg, 2),
            "pass_count": passed,
            "row_count": len(cleaned),
            "dropped_count": len(dropped),
        }

    df = pd.DataFrame(cleaned)
    return {
        "backend": "pandas",
        "avg": round(float(df["score"].mean()), 2),
        "pass_count": int((df["score"] >= 80).sum()),
        "row_count": int(len(df)),
        "dropped_count": len(dropped),
    }

def build_test_cases():
    cases = [
        (
            "baseline",
            [
                {"name": "A", "score": 72},
                {"name": "B", "score": 88},
                {"name": "C", "score": 91},
            ],
        ),
    ]
    if EXAMPLE_VARIANT >= 2:
        cases.append(
            (
                "string_scores",
                [
                    {"name": "D", "score": "84"},
                    {"name": "E", "score": "79.5"},
                    {"name": "F", "score": "92"},
                ],
            )
        )
    if EXAMPLE_VARIANT >= 3:
        cases.append(
            (
                "missing_values",
                [
                    {"name": "G", "score": 81},
                    {"name": "H", "score": None},
                    {"name": "I", "score": "err"},
                ],
            )
        )
    if EXAMPLE_VARIANT >= 4:
        cases.append(
            (
                "edge_threshold",
                [
                    {"name": "J", "score": 79.99},
                    {"name": "K", "score": 80},
                    {"name": "L", "score": 80.01},
                ],
            )
        )
    if EXAMPLE_VARIANT >= 5:
        cases.append(
            (
                "mixed_inputs",
                [
                    {"name": "M", "score": "100"},
                    {"name": "N", "score": "-5"},
                    {"name": " ", "score": 87.2},
                    {"name": "P", "score": "not-a-number"},
                ],
            )
        )
    return cases

def main():
    print("오늘 주제:", TOPIC)
    reports = []
    for name, rows in build_test_cases():
        summary = summarize_scores(rows)
        summary["case"] = name
        reports.append(summary)
        print(f"[{name}] 요약:", summary)
    return {"variant": EXAMPLE_VARIANT, "case_count": len(reports), "reports": reports}

if __name__ == "__main__":
    main()
