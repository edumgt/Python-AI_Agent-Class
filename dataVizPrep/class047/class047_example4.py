# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class047 example4: NumPy 기초 · 단계 3/4 실전 검증 [class047]"""

TOPIC = "NumPy 기초 · 단계 3/4 실전 검증 [class047]"
EXAMPLE_TEMPLATE = "numpy"

try:
    import numpy as np
except ImportError:
    np = None

def compute_stats(values):
    if np is None:
        avg = sum(values) / len(values)
        var = sum((v - avg) ** 2 for v in values) / len(values)
        return {"mean": round(avg, 4), "std": round(var ** 0.5, 4), "backend": "python"}
    arr = np.array(values, dtype=float)
    return {
        "mean": round(float(arr.mean()), 4),
        "std": round(float(arr.std()), 4),
        "backend": "numpy",
    }

def main():
    print("오늘 주제:", TOPIC)
    result = compute_stats([0.3, 0.4, 0.45, 0.5, 0.65])
    print("통계:", result)
    return result

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
