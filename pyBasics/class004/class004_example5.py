# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class004 example5: Python 기초 시작: 변수와 출력 첫 실행 (class004) · 단계 1/1 입문 이해 [class004]"""

TOPIC = "Python 기초 시작: 변수와 출력 첫 실행 (class004) · 단계 1/1 입문 이해 [class004]"
EXAMPLE_TEMPLATE = "variables"
EXAMPLE_VARIANT = 5

def infer_schema(record):
    return {k: type(v).__name__ for k, v in record.items()}

def parse_bool(value):
    text = str(value).strip().lower()
    return text in {"1", "true", "yes", "y"}

def normalize_record(record):
    name = str(record["name"]).strip()
    age = int(record["age"])
    score = float(record["score"])
    active = parse_bool(record["active"])
    level = "pass" if score >= 80 else "retry"
    return {
        "name": name,
        "age": age,
        "score": score,
        "active": active,
        "level": level,
    }

def format_report(row):
    return (
        f"{row['name']}({row['age']}) "
        f"score={row['score']:.1f} active={row['active']} level={row['level']}"
    )

def build_test_cases():
    cases = [
        {
            "case": "baseline",
            "name": "  민수  ",
            "age": "19",
            "score": "91.5",
            "active": "1",
        }
    ]
    if EXAMPLE_VARIANT >= 2:
        cases.append(
            {
                "case": "string_bool",
                "name": "지연",
                "age": "20",
                "score": "79.9",
                "active": "yes",
            }
        )
    if EXAMPLE_VARIANT >= 3:
        cases.append(
            {
                "case": "boundary",
                "name": "하늘",
                "age": "18",
                "score": "80",
                "active": "false",
            }
        )
    if EXAMPLE_VARIANT >= 4:
        cases.append(
            {
                "case": "high_score",
                "name": "도윤",
                "age": "22",
                "score": "99.4",
                "active": "True",
            }
        )
    if EXAMPLE_VARIANT >= 5:
        cases.append(
            {
                "case": "invalid_age",
                "name": "오류케이스",
                "age": "N/A",
                "score": "60",
                "active": "0",
            }
        )
    return cases

def main():
    print("오늘 주제:", TOPIC)
    reports = []
    errors = []
    for raw in build_test_cases():
        case_name = raw["case"]
        try:
            normalized = normalize_record(raw)
            normalized["case"] = case_name
            normalized["schema"] = infer_schema(normalized)
            normalized["summary"] = format_report(normalized)
            reports.append(normalized)
            print(f"[{case_name}] 정규화:", normalized["summary"])
        except (TypeError, ValueError) as exc:
            error = {"case": case_name, "error": str(exc)}
            errors.append(error)
            print(f"[{case_name}] 오류:", error)
    return {"variant": EXAMPLE_VARIANT, "success": len(reports), "errors": errors}

def ops_readiness_check():
    return {
        "risk": "입력 검증 실패 시 기본값/재입력 정책을 정의하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
