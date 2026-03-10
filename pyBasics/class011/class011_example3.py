# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class011 example3: 연산자와 조건문 · 단계 3/4 실전 검증 [class011]"""

TOPIC = "연산자와 조건문 · 단계 3/4 실전 검증 [class011]"
EXAMPLE_TEMPLATE = "condition"
EXAMPLE_VARIANT = 3

def classify_price(amount):
    if amount >= 100000:
        return "premium"
    if amount >= 50000:
        return "standard"
    return "starter"

def discount_policy(order):
    base = classify_price(order["amount"])
    if order["member"] and order["coupon"]:
        rate = 0.18
    elif order["member"] or order["coupon"]:
        rate = 0.1
    else:
        rate = 0.0
    if order["amount"] < 0:
        return {"status": "invalid", "rate": 0.0, "final": 0}
    final = int(order["amount"] * (1 - rate))
    return {"status": base, "rate": rate, "final": final}

def build_test_cases():
    cases = [{"name": "A", "amount": 120000, "member": True, "coupon": False}]
    if EXAMPLE_VARIANT >= 2:
        cases.append({"name": "B", "amount": 85000, "member": False, "coupon": True})
    if EXAMPLE_VARIANT >= 3:
        cases.append({"name": "C", "amount": 42000, "member": False, "coupon": False})
    if EXAMPLE_VARIANT >= 4:
        cases.append({"name": "D", "amount": 50000, "member": True, "coupon": True})
    if EXAMPLE_VARIANT >= 5:
        cases.append({"name": "E", "amount": -1000, "member": True, "coupon": True})
    return cases

def main():
    print("오늘 주제:", TOPIC)
    outputs = []
    for case in build_test_cases():
        result = discount_policy(case)
        row = {**case, **result}
        outputs.append(row)
        print("판정:", row)
    invalid_count = sum(1 for row in outputs if row["status"] == "invalid")
    return {"variant": EXAMPLE_VARIANT, "case_count": len(outputs), "invalid_count": invalid_count}

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "중첩 조건을 함수 분리로 리팩터링하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
