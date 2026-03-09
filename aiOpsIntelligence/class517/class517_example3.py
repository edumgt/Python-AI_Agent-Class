# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class517 example3: AIOps 관측성·이상탐지·자동복구 · 단계 2/5 기초 구현 [class517]"""

TOPIC = "AIOps 관측성·이상탐지·자동복구 · 단계 2/5 기초 구현 [class517]"
EXAMPLE_TEMPLATE = "data_preprocess"

from datetime import datetime

def clean_rows(rows):
    cleaned = []
    for row in rows:
        text = row["text"].strip().lower()
        date_obj = datetime.strptime(row["date"], "%Y-%m-%d")
        cleaned.append({"text": text, "month": date_obj.month})
    return cleaned

def main():
    rows = [
        {"text": "  Hello AI  ", "date": "2026-03-01"},
        {"text": "Data  Prep ", "date": "2026-04-02"},
    ]
    print("오늘 주제:", TOPIC)
    print(clean_rows(rows))


def self_check():
    return [
        "입력/출력 형식을 다시 설명할 수 있는가?",
        "오류 상황 1가지를 직접 만들어 테스트했는가?",
        "핵심 로직을 함수 단위로 분리했는가?",
    ]

def challenge_case():
    return {
        "task": "같은 로직을 새로운 입력 데이터로 재실행",
        "goal": "결과 차이를 한 문장으로 요약",
    }

if __name__ == "__main__":
    main()
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
