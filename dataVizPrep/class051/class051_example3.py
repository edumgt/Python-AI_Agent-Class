# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class051 example3: Pandas 데이터프레임 기초 · 단계 3/4 실전 검증 [class051]"""

TOPIC = "Pandas 데이터프레임 기초 · 단계 3/4 실전 검증 [class051]"
EXAMPLE_TEMPLATE = "pandas"

try:
    import pandas as pd
except ImportError:
    pd = None

def summarize_scores(rows):
    if pd is None:
        avg = sum(r["score"] for r in rows) / len(rows)
        passed = sum(1 for r in rows if r["score"] >= 80)
        return {"backend": "python", "avg": round(avg, 2), "pass_count": passed}

    df = pd.DataFrame(rows)
    return {
        "backend": "pandas",
        "avg": round(float(df["score"].mean()), 2),
        "pass_count": int((df["score"] >= 80).sum()),
    }

def main():
    print("오늘 주제:", TOPIC)
    rows = [{"name": "A", "score": 72}, {"name": "B", "score": 88}, {"name": "C", "score": 91}]
    summary = summarize_scores(rows)
    print("요약:", summary)
    return summary

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
