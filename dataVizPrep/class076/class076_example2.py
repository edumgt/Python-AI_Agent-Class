# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class076 example2: Seaborn/실전 차트 해석 · 단계 4/4 운영 최적화 [class076]"""

TOPIC = "Seaborn/실전 차트 해석 · 단계 4/4 운영 최적화 [class076]"
EXAMPLE_TEMPLATE = "visualization"

from pathlib import Path

def save_chart(points):
    out = Path(__file__).with_name("class076_plot.png")
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

def extension_mission():
    return {
        "mission": "입력값 2세트를 비교하고 차이를 기록하세요.",
        "check": "예외 케이스 1개를 추가해 방어 로직을 검증하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
