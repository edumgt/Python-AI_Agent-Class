# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class051 example4: Pandas 데이터프레임 기초 · 단계 3/4 실전 검증 [class051]"""

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
