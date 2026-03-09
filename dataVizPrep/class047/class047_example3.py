# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class047 example3: NumPy 기초 · 단계 3/4 실전 검증 [class047]"""

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
