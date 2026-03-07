# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class072 example3: Matplotlib 시각화 기초"""

TOPIC = "Matplotlib 시각화 기초"
EXAMPLE_TEMPLATE = "visualization"

from pathlib import Path
import matplotlib.pyplot as plt

def make_plot():
    x = [1, 2, 3, 4]
    y = [2, 4, 3, 5]
    plt.figure(figsize=(4, 3))
    plt.plot(x, y, marker="o")
    plt.title(TOPIC)
    out = Path(__file__).with_name("class072_plot.png")
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out

def main():
    print("오늘 주제:", TOPIC)
    print("그래프 저장:", make_plot())


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
