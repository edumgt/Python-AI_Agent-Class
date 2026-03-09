# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class074 example5: Seaborn/실전 차트 해석 · 단계 2/4 기초 구현 [class074]"""

TOPIC = "Seaborn/실전 차트 해석 · 단계 2/4 기초 구현 [class074]"
EXAMPLE_TEMPLATE = "visualization"

from pathlib import Path

def save_chart(points):
    out = Path(__file__).with_name("class074_plot.png")
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

def ops_readiness_check():
    return {
        "risk": "운영 체크리스트(모니터링/알림/복구)를 정의하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
