# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class124 example2: 딥러닝 학습 구조"""

TOPIC = "딥러닝 학습 구조"
EXAMPLE_TEMPLATE = "deep_learning"

def relu(x):
    return x if x > 0 else 0

def dense_step(inputs, weights, bias):
    total = sum(i * w for i, w in zip(inputs, weights)) + bias
    return relu(total)

def main():
    print("오늘 주제:", TOPIC)
    out = dense_step([0.8, -0.2, 0.5], [0.4, 0.6, 0.3], 0.1)
    print("뉴런 출력:", round(out, 3))


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
