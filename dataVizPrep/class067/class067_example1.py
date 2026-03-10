# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class067 example1: 데이터 병합과 변환 · 단계 3/4 실전 검증 [class067]"""

TOPIC = "데이터 병합과 변환 · 단계 3/4 실전 검증 [class067]"
EXAMPLE_TEMPLATE = "data_preprocess"
EXAMPLE_VARIANT = 1

from datetime import datetime

def parse_amount(raw):
    if raw is None:
        return None
    text = str(raw).strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None

def parse_date(raw):
    text = str(raw).strip()
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return None

def clean_rows(rows):
    cleaned = []
    rejected = []
    for idx, row in enumerate(rows, start=1):
        text = str(row.get("text", "")).strip().lower()
        amount = parse_amount(row.get("amount"))
        when = parse_date(row.get("date"))
        if not text or amount is None or when is None:
            rejected.append(
                {
                    "row": idx,
                    "text": row.get("text"),
                    "amount": row.get("amount"),
                    "date": row.get("date"),
                }
            )
            continue
        cleaned.append({"text": text, "amount": amount, "month": when.month})
    return cleaned, rejected

def summarize(rows):
    if not rows:
        return {"rows": 0, "total": 0.0, "avg": 0.0, "min": None, "max": None}
    total = round(sum(r["amount"] for r in rows), 2)
    avg = round(total / len(rows), 2)
    min_amount = round(min(r["amount"] for r in rows), 2)
    max_amount = round(max(r["amount"] for r in rows), 2)
    return {"rows": len(rows), "total": total, "avg": avg, "min": min_amount, "max": max_amount}

def build_test_cases():
    cases = [
        (
            "baseline",
            [
                {"text": "  GPU Server  ", "amount": "1200", "date": "2026-03-01"},
                {"text": "Monitoring  ", "amount": "450", "date": "2026-03-12"},
            ],
        ),
    ]
    if EXAMPLE_VARIANT >= 2:
        cases.append(
            (
                "zero_and_spaces",
                [
                    {"text": "  cache  ", "amount": "0", "date": "2026-03-20"},
                    {"text": "  API Gateway ", "amount": "99.5", "date": "2026-03-21"},
                ],
            )
        )
    if EXAMPLE_VARIANT >= 3:
        cases.append(
            (
                "invalid_rows",
                [
                    {"text": "STT", "amount": "300", "date": "2026-03-10"},
                    {"text": "", "amount": "180", "date": "2026-03-11"},
                    {"text": "TTS", "amount": "not-number", "date": "2026-03-12"},
                    {"text": "Batch", "amount": "200", "date": "2026/03/13"},
                ],
            )
        )
    if EXAMPLE_VARIANT >= 4:
        cases.append(
            (
                "signed_amounts",
                [
                    {"text": "refund", "amount": "-120", "date": "2026-02-01"},
                    {"text": "usage", "amount": "320", "date": "2026-02-02"},
                    {"text": "credit", "amount": "-40", "date": "2026-02-03"},
                ],
            )
        )
    if EXAMPLE_VARIANT >= 5:
        cases.append(
            (
                "mixed_months",
                [
                    {"text": "alpha", "amount": "1,200", "date": "2026-01-05"},
                    {"text": "beta", "amount": "860.75", "date": "2026-02-11"},
                    {"text": "gamma", "amount": "420", "date": "2026-02-17"},
                    {"text": "delta", "amount": "1040", "date": "2026-03-09"},
                ],
            )
        )
    return cases

def main():
    print("오늘 주제:", TOPIC)
    results = []
    for case_name, raw in build_test_cases():
        cleaned, rejected = clean_rows(raw)
        report = summarize(cleaned)
        report.update(
            {
                "case": case_name,
                "rejected_rows": len(rejected),
                "months": sorted({row["month"] for row in cleaned}),
            }
        )
        results.append(report)
        print(f"[{case_name}] 정제 데이터:", cleaned)
        print(f"[{case_name}] 제외 데이터:", rejected)
        print(f"[{case_name}] 요약:", report)

    total_valid = sum(item["rows"] for item in results)
    total_rejected = sum(item["rejected_rows"] for item in results)
    return {"variant": EXAMPLE_VARIANT, "case_count": len(results), "valid_rows": total_valid, "rejected_rows": total_rejected}

if __name__ == "__main__":
    main()
