# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class017 example2: 함수와 모듈 · 단계 1/4 입문 이해 [class017]"""

TOPIC = "함수와 모듈 · 단계 1/4 입문 이해 [class017]"
EXAMPLE_TEMPLATE = "function_module"
EXAMPLE_VARIANT = 2

def grade(score, pass_line=70):
    return "PASS" if score >= pass_line else "RETRY"

def summarize_scores(*scores):
    if not scores:
        return {"avg": 0.0, "max": 0.0, "min": 0.0}
    return {
        "avg": round(sum(scores) / len(scores), 2),
        "max": max(scores),
        "min": min(scores),
    }

def build_profile(name, **kwargs):
    profile = {"name": name}
    profile.update(kwargs)
    return profile

def apply_pipeline(values, *funcs):
    result = list(values)
    for fn in funcs:
        result = [fn(v) for v in result]
    return result

def build_test_cases():
    cases = [("baseline", [72, 88, 91])]
    if EXAMPLE_VARIANT >= 2:
        cases.append(("mixed", [61, 77, 84, 95]))
    if EXAMPLE_VARIANT >= 3:
        cases.append(("boundary", [70, 70, 69]))
    if EXAMPLE_VARIANT >= 4:
        cases.append(("short", [100]))
    if EXAMPLE_VARIANT >= 5:
        cases.append(("wide", [32, 58, 74, 81, 93]))
    return cases

def main():
    print("오늘 주제:", TOPIC)
    reports = []
    for case_name, scores in build_test_cases():
        stats = summarize_scores(*scores)
        labels = [grade(score, pass_line=75) for score in scores]
        curved = apply_pipeline(
            scores,
            lambda v: v + 3,
            lambda v: min(v, 100),
        )
        profile = build_profile(
            case_name,
            count=len(scores),
            avg=stats["avg"],
            pass_count=sum(1 for label in labels if label == "PASS"),
        )
        report = {
            "case": case_name,
            "stats": stats,
            "labels": labels,
            "curved": curved,
            "profile": profile,
        }
        reports.append(report)
        print(f"[{case_name}] 함수 리포트:", report)
    return {"variant": EXAMPLE_VARIANT, "case_count": len(reports)}

def extension_mission():
    return {
        "mission": "기본값 인자, 가변 인자, lambda를 각각 1회 이상 사용하세요.",
        "check": "함수 입력/출력 계약을 테스트로 검증하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
