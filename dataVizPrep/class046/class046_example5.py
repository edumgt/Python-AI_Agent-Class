# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class046 example5: NumPy 기초 · 단계 2/4 기초 구현 [class046]"""

TOPIC = "NumPy 기초 · 단계 2/4 기초 구현 [class046]"
EXAMPLE_TEMPLATE = "numpy"
EXAMPLE_VARIANT = 5

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

def ops_readiness_check():
    return {
        "risk": "운영 체크리스트(모니터링/알림/복구)를 정의하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
