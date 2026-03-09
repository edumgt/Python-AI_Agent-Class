# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class013 example1: 반복문과 흐름제어 · 단계 1/4 입문 이해 [class013]"""

TOPIC = "반복문과 흐름제어 · 단계 1/4 입문 이해 [class013]"
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

if __name__ == "__main__":
    main()
