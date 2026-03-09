# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class511 example1: LLMOps/RAG 서비스 품질관리 · 단계 1/5 입문 이해 [class511]"""

TOPIC = "LLMOps/RAG 서비스 품질관리 · 단계 1/5 입문 이해 [class511]"
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
