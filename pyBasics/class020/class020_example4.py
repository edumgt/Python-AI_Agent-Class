# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class020 example4: 함수와 모듈 · 단계 4/4 운영 최적화 [class020]"""

TOPIC = "함수와 모듈 · 단계 4/4 운영 최적화 [class020]"
EXAMPLE_TEMPLATE = "function_module"
EXAMPLE_VARIANT = 4

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

def mini_project_plan():
    return {
        "scenario": "작은 기능 3개를 함수 모듈로 분리해 재사용하세요.",
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
