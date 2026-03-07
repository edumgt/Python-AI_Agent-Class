# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class279 example1: 모델 추론 및 튜닝"""

TOPIC = "모델 추론 및 튜닝"
EXAMPLE_TEMPLATE = "ml"

def make_data():
    return [(1, 52), (2, 61), (3, 70), (4, 82)]

def mean_predict(train):
    return sum(y for _, y in train) / len(train)

def mae(train, pred):
    return sum(abs(y - pred) for _, y in train) / len(train)

def main():
    data = make_data()
    pred = mean_predict(data)
    print("오늘 주제:", TOPIC)
    print("기본 예측값:", round(pred, 2))
    print("MAE:", round(mae(data, pred), 2))


if __name__ == "__main__":
    main()
