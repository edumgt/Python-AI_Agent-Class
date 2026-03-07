# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class069 example2: Matplotlib 시각화 기초"""

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
    out = Path(__file__).with_name("class069_plot.png")
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out

def main():
    print("오늘 주제:", TOPIC)
    print("그래프 저장:", make_plot())


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
