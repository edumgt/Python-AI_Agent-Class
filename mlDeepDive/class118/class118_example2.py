# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class118 example2: 신경망 기초 · 단계 4/5 실전 검증 [class118]"""

TOPIC = "신경망 기초 · 단계 4/5 실전 검증 [class118]"
EXAMPLE_TEMPLATE = "deep_learning"

def relu(x):
    return x if x > 0 else 0.0

def dense_forward(inputs, weights, bias):
    z = sum(i * w for i, w in zip(inputs, weights)) + bias
    return relu(z)

def predict_batch(batch, weights, bias):
    return [round(dense_forward(x, weights, bias), 4) for x in batch]

def main():
    print("오늘 주제:", TOPIC)
    batch = [[0.2, 0.5, 0.1], [0.4, 0.4, 0.2], [0.9, 0.1, 0.3]]
    weights = [0.6, 0.3, 0.8]
    bias = -0.2
    preds = predict_batch(batch, weights, bias)
    report = {"predictions": preds, "max_pred": max(preds)}
    print("추론 결과:", report)
    return report

def extension_mission():
    return {
        "mission": "가중치와 bias를 2세트로 바꿔 출력 분포를 비교하세요.",
        "check": "활성화 함수 전/후 값을 표로 정리하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
