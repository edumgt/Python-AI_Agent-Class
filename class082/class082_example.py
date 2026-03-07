# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class082 쉬운 예제: ML/DL 개요와 문제정의"""

TOPIC = "ML/DL 개요와 문제정의"

def average_predictor(samples):
    total = sum(score for _, score in samples)
    return total / len(samples)

def mae(samples, prediction):
    errors = [abs(score - prediction) for _, score in samples]
    return sum(errors) / len(errors)

def main():
    data = [(1, 50), (2, 60), (3, 70), (4, 80)]
    pred = average_predictor(data)
    error = mae(data, pred)
    print("오늘 주제:", TOPIC)
    print("예측값(평균):", round(pred, 2))
    print("평균 절대 오차:", round(error, 2))

if __name__ == "__main__":
    main()
