# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class280 example3: 모델 추론 및 튜닝 · 단계 4/6 응용 확장 [class280]"""

TOPIC = "모델 추론 및 튜닝 · 단계 4/6 응용 확장 [class280]"
EXAMPLE_TEMPLATE = "ml"

def make_dataset():
    return [(1, 52), (2, 61), (3, 70), (4, 82), (5, 91)]

def fit_linear(points):
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in points)
    den = sum((x - mean_x) ** 2 for x in xs)
    slope = num / den
    bias = mean_y - slope * mean_x
    return slope, bias

def mae(points, slope, bias):
    errors = [abs(y - (slope * x + bias)) for x, y in points]
    return sum(errors) / len(errors)

def main():
    print("오늘 주제:", TOPIC)
    points = make_dataset()
    slope, bias = fit_linear(points)
    metric = round(mae(points, slope, bias), 3)
    report = {"slope": round(slope, 3), "bias": round(bias, 3), "mae": metric}
    print("평가 리포트:", report)
    return report

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "검증 데이터를 따로 두고 과적합 징후를 기록하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
