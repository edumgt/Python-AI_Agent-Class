# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class080 example3: Agent 시스템 통합 구현 · 단계 4/4 운영 최적화 [class080]"""

TOPIC = "Agent 시스템 통합 구현 · 단계 4/4 운영 최적화 [class080]"
EXAMPLE_TEMPLATE = "generic"
EXAMPLE_VARIANT = 3

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
