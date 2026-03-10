# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class011 example2: 연산자와 조건문 · 단계 3/4 실전 검증 [class011]"""

TOPIC = "연산자와 조건문 · 단계 3/4 실전 검증 [class011]"
EXAMPLE_TEMPLATE = "condition"
EXAMPLE_VARIANT = 2

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

def extension_mission():
    return {
        "mission": "if/elif/else 경계값을 5개 이상 테스트하세요.",
        "check": "잘못된 조건식 우선순위를 괄호로 바로잡아 비교하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
