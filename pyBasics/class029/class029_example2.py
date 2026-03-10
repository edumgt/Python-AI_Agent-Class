# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class029 example2: 웹 프론트엔드 기초 (HTML/CSS/JS) · 단계 1/2 입문 이해 [class029]"""

TOPIC = "웹 프론트엔드 기초 (HTML/CSS/JS) · 단계 1/2 입문 이해 [class029]"
EXAMPLE_TEMPLATE = "generic"
EXAMPLE_VARIANT = 2

def solve_in_steps(task):
    return [
        f"1단계: {task} 요구사항 정리",
        "2단계: 입력 검증과 핵심 로직 분리",
        "3단계: 테스트 입력을 단계별로 확장",
    ]

def build_test_cases():
    cases = [
        {"name": "baseline", "latency_ms": 380, "error_rate": 0.01, "coverage": 0.82},
    ]
    if EXAMPLE_VARIANT >= 2:
        cases.append({"name": "high_latency", "latency_ms": 820, "error_rate": 0.02, "coverage": 0.84})
    if EXAMPLE_VARIANT >= 3:
        cases.append({"name": "high_error", "latency_ms": 410, "error_rate": 0.09, "coverage": 0.81})
    if EXAMPLE_VARIANT >= 4:
        cases.append({"name": "low_coverage", "latency_ms": 360, "error_rate": 0.015, "coverage": 0.62})
    if EXAMPLE_VARIANT >= 5:
        cases.append({"name": "balanced", "latency_ms": 295, "error_rate": 0.008, "coverage": 0.9})
    return cases

def evaluate_case(case):
    score = 0
    if case["latency_ms"] <= 500:
        score += 1
    if case["error_rate"] <= 0.03:
        score += 1
    if case["coverage"] >= 0.8:
        score += 1
    return {
        "name": case["name"],
        "score": score,
        "pass": score >= 2,
        "latency_ms": case["latency_ms"],
        "error_rate": case["error_rate"],
        "coverage": case["coverage"],
    }

def main():
    print("오늘 주제:", TOPIC)
    for line in solve_in_steps(TOPIC):
        print(line)

    reports = [evaluate_case(case) for case in build_test_cases()]
    for report in reports:
        print("케이스 결과:", report)

    pass_count = sum(1 for report in reports if report["pass"])
    return {"variant": EXAMPLE_VARIANT, "case_count": len(reports), "pass_count": pass_count}

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
