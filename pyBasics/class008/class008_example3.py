# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class008 example3: 변수와 자료형 · 단계 4/4 운영 최적화 [class008]"""

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
