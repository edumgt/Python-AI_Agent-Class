# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class008 example4: 변수와 자료형 · 단계 4/4 운영 최적화 [class008]"""

TOPIC = "변수와 자료형 · 단계 4/4 운영 최적화 [class008]"
EXAMPLE_TEMPLATE = "variables"
EXAMPLE_VARIANT = 4

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

def mini_project_plan():
    return {
        "scenario": "기본 문법 검증기(타입/연산자/포맷) 함수를 작성하세요.",
        "steps": [
            "1) baseline 실행",
            "2) 개선안 적용",
            "3) 지표/로그 비교",
        ],
        "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("미니 프로젝트:", mini_project_plan())
