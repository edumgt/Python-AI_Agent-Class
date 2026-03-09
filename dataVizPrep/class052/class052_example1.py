# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class052 example1: Pandas 데이터프레임 기초 · 단계 4/4 운영 최적화 [class052]"""

TOPIC = "Pandas 데이터프레임 기초 · 단계 4/4 운영 최적화 [class052]"
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

if __name__ == "__main__":
    main()
