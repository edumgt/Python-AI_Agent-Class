# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class072 example1: Matplotlib 시각화 기초"""

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


if __name__ == "__main__":
    main()
