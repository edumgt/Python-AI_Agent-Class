# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class244 쉬운 예제: STT 데이터 라벨링"""

TOPIC = "STT 데이터 라벨링"

def filter_short_clips(items, max_seconds):
    return [item for item in items if item["seconds"] <= max_seconds]

def average_seconds(items):
    return sum(item["seconds"] for item in items) / len(items)

def main():
    clips = [
        {"id": "utt1", "text": "안녕하세요", "seconds": 1.2},
        {"id": "utt2", "text": "오늘도 화이팅", "seconds": 2.4},
        {"id": "utt3", "text": "파이썬은 재밌다", "seconds": 1.8},
    ]
    short_clips = filter_short_clips(clips, 2.0)
    print("오늘 주제:", TOPIC)
    print("짧은 발화:", [item["id"] for item in short_clips])
    print("평균 길이:", round(average_seconds(clips), 2))

if __name__ == "__main__":
    main()
