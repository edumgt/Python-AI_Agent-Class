# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class020 example3: 함수와 모듈 · 단계 4/4 운영 최적화 [class020]"""

TOPIC = "함수와 모듈 · 단계 4/4 운영 최적화 [class020]"
EXAMPLE_TEMPLATE = "function_module"
EXAMPLE_VARIANT = 3

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

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "함수형 파이프라인(map/filter 또는 lambda)을 확장하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
