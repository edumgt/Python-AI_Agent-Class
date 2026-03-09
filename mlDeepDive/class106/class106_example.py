# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class106 example1: 특성공학과 전처리 · 단계 2/5 기초 구현 [class106]"""

TOPIC = "특성공학과 전처리 · 단계 2/5 기초 구현 [class106]"
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

if __name__ == "__main__":
    main()
