# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class519 example2: AIOps 관측성·이상탐지·자동복구 · 단계 4/5 실전 검증 [class519]"""

TOPIC = "AIOps 관측성·이상탐지·자동복구 · 단계 4/5 실전 검증 [class519]"
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
