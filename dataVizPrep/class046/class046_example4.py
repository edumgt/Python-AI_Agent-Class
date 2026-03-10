# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class046 example4: NumPy 기초 · 단계 2/4 기초 구현 [class046]"""

TOPIC = "NumPy 기초 · 단계 2/4 기초 구현 [class046]"
EXAMPLE_TEMPLATE = "numpy"
EXAMPLE_VARIANT = 4

try:
    import numpy as np
except ImportError:
    np = None

def compute_stats(values):
    if not values:
        raise ValueError("values must not be empty")
    if np is None:
        avg = sum(values) / len(values)
        var = sum((v - avg) ** 2 for v in values) / len(values)
        return {"mean": round(avg, 4), "std": round(var ** 0.5, 4), "backend": "python"}
    arr = np.array(values, dtype=float)
    return {
        "mean": round(float(arr.mean()), 4),
        "std": round(float(arr.std()), 4),
        "backend": "numpy",
    }

def build_test_cases():
    cases = [("baseline", [0.3, 0.4, 0.45, 0.5, 0.65])]
    if EXAMPLE_VARIANT >= 2:
        cases.append(("signed_values", [-1.2, -0.2, 0.0, 0.5, 1.1]))
    if EXAMPLE_VARIANT >= 3:
        cases.append(("with_outlier", [10, 10.2, 9.9, 10.1, 45]))
    if EXAMPLE_VARIANT >= 4:
        cases.append(("wide_range", [0.001, 1, 10, 100, 250]))
    if EXAMPLE_VARIANT >= 5:
        cases.append(("tiny_decimals", [0.1001, 0.1002, 0.1004, 0.1003, 0.1002]))
    return cases

def main():
    print("오늘 주제:", TOPIC)
    reports = []
    for name, values in build_test_cases():
        stats = compute_stats(values)
        stats["case"] = name
        stats["size"] = len(values)
        reports.append(stats)
        print(f"[{name}] 통계:", stats)

    largest = max(reports, key=lambda x: x["std"])
    return {
        "variant": EXAMPLE_VARIANT,
        "case_count": len(reports),
        "largest_std_case": largest["case"],
        "backend": reports[0]["backend"] if reports else "unknown",
    }

def mini_project_plan():
    return {
        "scenario": "미니 프로젝트 형태로 실행 로그를 구조화하세요.",
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
