# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class058 example2: 문자열/날짜 전처리"""

TOPIC = "문자열/날짜 전처리"
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


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
