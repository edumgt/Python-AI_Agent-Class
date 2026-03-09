# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class016 example3: 반복문과 흐름제어 · 단계 4/4 운영 최적화 [class016]"""

TOPIC = "반복문과 흐름제어 · 단계 4/4 운영 최적화 [class016]"
EXAMPLE_TEMPLATE = "loop"

def rolling_average(values, window):
    result = []
    for idx in range(len(values)):
        start = max(0, idx - window + 1)
        chunk = values[start : idx + 1]
        result.append(round(sum(chunk) / len(chunk), 2))
    return result

def main():
    print("오늘 주제:", TOPIC)
    values = [12, 15, 13, 20, 19, 23]
    trend = rolling_average(values, window=3)
    print("원본:", values)
    print("이동평균:", trend)
    return {"last_avg": trend[-1], "points": len(values)}

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
