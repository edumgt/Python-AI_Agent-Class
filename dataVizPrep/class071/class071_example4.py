# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class071 example4: Matplotlib 시각화 기초 · 단계 3/4 실전 검증 [class071]"""

TOPIC = "Matplotlib 시각화 기초 · 단계 3/4 실전 검증 [class071]"
EXAMPLE_TEMPLATE = "visualization"
EXAMPLE_VARIANT = 4

from pathlib import Path
import re

def sanitize_case_name(name):
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", name).strip("_") or "case"

def save_chart(points, case_name):
    token = sanitize_case_name(case_name)
    out = Path(__file__).with_name(f"class071_plot_{token}.png")
    try:
        import matplotlib.pyplot as plt

        x = [idx + 1 for idx, _ in enumerate(points)]
        y = [v for _, v in points]
        plt.figure(figsize=(5, 3))
        plt.plot(x, y, marker="o")
        plt.title(f"{TOPIC} | {case_name}")
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

def summarize_points(points):
    values = [float(v) for _, v in points]
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "delta": round(values[-1] - values[0], 2),
    }

def build_test_cases():
    cases = [
        ("baseline_uptrend", [("week1", 61), ("week2", 67), ("week3", 73), ("week4", 78)]),
    ]
    if EXAMPLE_VARIANT >= 2:
        cases.append(("with_dip", [("w1", 80), ("w2", 72), ("w3", 76), ("w4", 88)]))
    if EXAMPLE_VARIANT >= 3:
        cases.append(("negative_values", [("q1", -4), ("q2", 2), ("q3", 5), ("q4", -1)]))
    if EXAMPLE_VARIANT >= 4:
        cases.append(("flat_signal", [("h1", 5), ("h2", 5), ("h3", 5), ("h4", 5)]))
    if EXAMPLE_VARIANT >= 5:
        cases.append(("with_outlier", [("d1", 11), ("d2", 10), ("d3", 40), ("d4", 12)]))
    return cases

def main():
    print("오늘 주제:", TOPIC)
    outputs = []
    for case_name, points in build_test_cases():
        out, mode = save_chart(points, case_name=case_name)
        summary = summarize_points(points)
        outputs.append({"case": case_name, "output": out.name, "mode": mode, "summary": summary})
        print(f"[{case_name}] 출력 파일:", out.name, "| 요약:", summary)
    return {"variant": EXAMPLE_VARIANT, "case_count": len(outputs), "outputs": outputs}

def mini_project_plan():
    return {
        "scenario": "미니 프로젝트 형태로 실행 로그를 구조화하세요.",
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
