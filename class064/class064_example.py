# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class064 example1: 그룹화와 집계"""

TOPIC = "그룹화와 집계"
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


if __name__ == "__main__":
    main()
