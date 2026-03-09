# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class124 example5: 딥러닝 학습 구조 · 단계 5/5 운영 최적화 [class124]"""

TOPIC = "딥러닝 학습 구조 · 단계 5/5 운영 최적화 [class124]"
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

def ops_readiness_check():
    return {
        "risk": "추론 실패 시 fallback 모델 호출 절차를 정의하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
