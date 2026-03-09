# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class124 example4: 딥러닝 학습 구조 · 단계 5/5 운영 최적화 [class124]"""

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

def mini_project_plan():
    return {
        "scenario": "간단한 배치 추론 로그(입력/출력/latency)를 저장하세요.",
        "steps": [
            "1) baseline 실행",
            "2) 개선안 적용",
            "3) 지표/로그 비교",
        ],
        "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("미니 프로젝트:", mini_project_plan())
