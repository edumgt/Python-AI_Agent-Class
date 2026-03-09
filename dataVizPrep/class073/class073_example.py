# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class073 example1: Seaborn/실전 차트 해석 · 단계 1/4 입문 이해 [class073]"""

TOPIC = "Seaborn/실전 차트 해석 · 단계 1/4 입문 이해 [class073]"
EXAMPLE_TEMPLATE = "visualization"

from pathlib import Path

def save_chart(points):
    out = Path(__file__).with_name("class073_plot.png")
    try:
        import matplotlib.pyplot as plt

        x = [idx + 1 for idx, _ in enumerate(points)]
        y = [v for _, v in points]
        plt.figure(figsize=(5, 3))
        plt.plot(x, y, marker="o")
        plt.title(TOPIC)
        plt.xlabel("step")
        plt.ylabel("value")
        plt.tight_layout()
        plt.savefig(out)
        plt.close()
        mode = "matplotlib"
    except ImportError:
        text_out = out.with_suffix(".txt")
        text_out.write_text("\n".join(f"{k}: {v}" for k, v in points), encoding="utf-8")
        out = text_out
        mode = "text-fallback"
    return out, mode

def main():
    print("오늘 주제:", TOPIC)
    points = [("week1", 61), ("week2", 67), ("week3", 73), ("week4", 78)]
    out, mode = save_chart(points)
    print("출력 파일:", out.name)
    return {"output": out.name, "mode": mode}

if __name__ == "__main__":
    main()
