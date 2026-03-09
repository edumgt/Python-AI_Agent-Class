# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class047 example1: NumPy 기초 · 단계 3/4 실전 검증 [class047]"""

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

if __name__ == "__main__":
    main()
