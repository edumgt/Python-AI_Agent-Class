# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class058 example5: 문자열/날짜 전처리 · 단계 2/4 기초 구현 [class058]"""

TOPIC = "문자열/날짜 전처리 · 단계 2/4 기초 구현 [class058]"
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

def ops_readiness_check():
    return {
        "risk": "운영 체크리스트(모니터링/알림/복구)를 정의하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
