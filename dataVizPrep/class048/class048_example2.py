# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class048 example2: NumPy 기초 · 단계 4/4 운영 최적화 [class048]"""

TOPIC = "NumPy 기초 · 단계 4/4 운영 최적화 [class048]"
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
