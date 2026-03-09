# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class072 example3: Matplotlib 시각화 기초 · 단계 4/4 운영 최적화 [class072]"""

TOPIC = "Matplotlib 시각화 기초 · 단계 4/4 운영 최적화 [class072]"
EXAMPLE_TEMPLATE = "visualization"

from pathlib import Path

def save_chart(points):
    out = Path(__file__).with_name("class072_plot.png")
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

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "핵심 함수를 재사용 가능한 모듈로 분리하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
