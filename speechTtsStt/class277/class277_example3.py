# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class277 example3: 모델 추론 및 튜닝"""

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


def self_check():
    return [
        "입력/출력 형식을 다시 설명할 수 있는가?",
        "오류 상황 1가지를 직접 만들어 테스트했는가?",
        "핵심 로직을 함수 단위로 분리했는가?",
    ]

def challenge_case():
    return {
        "task": "같은 로직을 새로운 입력 데이터로 재실행",
        "goal": "결과 차이를 한 문장으로 요약",
    }

if __name__ == "__main__":
    main()
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
