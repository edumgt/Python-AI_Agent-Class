# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class049 example2: Pandas 데이터프레임 기초 · 단계 1/4 입문 이해 [class049]"""

TOPIC = "Pandas 데이터프레임 기초 · 단계 1/4 입문 이해 [class049]"
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
