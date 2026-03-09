# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class048 example5: NumPy 기초 · 단계 4/4 운영 최적화 [class048]"""

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
