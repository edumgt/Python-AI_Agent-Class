# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class057 example3: 문자열/날짜 전처리 · 단계 1/4 입문 이해 [class057]"""

TOPIC = "문자열/날짜 전처리 · 단계 1/4 입문 이해 [class057]"
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
