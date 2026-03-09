# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class068 example1: 데이터 병합과 변환 · 단계 4/4 운영 최적화 [class068]"""

TOPIC = "데이터 병합과 변환 · 단계 4/4 운영 최적화 [class068]"
EXAMPLE_TEMPLATE = "data_preprocess"

from datetime import datetime

def clean_rows(rows):
    cleaned = []
    for row in rows:
        text = row["text"].strip().lower()
        amount = float(row["amount"])
        when = datetime.strptime(row["date"], "%Y-%m-%d")
        cleaned.append({"text": text, "amount": amount, "month": when.month})
    return cleaned

def summarize(rows):
    total = round(sum(r["amount"] for r in rows), 2)
    avg = round(total / len(rows), 2)
    return {"rows": len(rows), "total": total, "avg": avg}

def main():
    print("오늘 주제:", TOPIC)
    raw = [
        {"text": "  GPU Server  ", "amount": "1200", "date": "2026-03-01"},
        {"text": "Monitoring  ", "amount": "450", "date": "2026-03-12"},
    ]
    cleaned = clean_rows(raw)
    report = summarize(cleaned)
    print("정제 데이터:", cleaned)
    print("요약:", report)
    return report

if __name__ == "__main__":
    main()
