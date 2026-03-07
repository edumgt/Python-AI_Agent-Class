# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class109 example2: 특성공학과 전처리"""

TOPIC = "특성공학과 전처리"
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


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
