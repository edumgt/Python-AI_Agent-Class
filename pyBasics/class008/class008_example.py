# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class008 example1: 변수와 자료형 · 단계 4/4 운영 최적화 [class008]"""

TOPIC = "변수와 자료형 · 단계 4/4 운영 최적화 [class008]"
EXAMPLE_TEMPLATE = "variables"

def infer_schema(record):
    return {k: type(v).__name__ for k, v in record.items()}

def normalize_record(record):
    return {
        "name": str(record["name"]).strip(),
        "score": float(record["score"]),
        "active": bool(record["active"]),
    }

def main():
    print("오늘 주제:", TOPIC)
    raw = {"name": "  민수  ", "score": "91.5", "active": 1}
    normalized = normalize_record(raw)
    print("원본 스키마:", infer_schema(raw))
    print("정규화 스키마:", infer_schema(normalized))
    return normalized

if __name__ == "__main__":
    main()
