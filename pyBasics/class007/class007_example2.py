# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class007 example2: 변수와 자료형 · 단계 3/4 실전 검증 [class007]"""

TOPIC = "변수와 자료형 · 단계 3/4 실전 검증 [class007]"
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
