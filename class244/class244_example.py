# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class244 example1: STT 데이터 라벨링"""

TOPIC = "STT 데이터 라벨링"
EXAMPLE_TEMPLATE = "speech"

def summarize_clips(clips):
    avg = sum(c["seconds"] for c in clips) / len(clips)
    short = [c["id"] for c in clips if c["seconds"] <= 2.0]
    return {"avg_seconds": round(avg, 2), "short_ids": short}

def main():
    clips = [
        {"id": "utt1", "seconds": 1.3, "text": "안녕하세요"},
        {"id": "utt2", "seconds": 2.4, "text": "오늘은 음성 실습"},
        {"id": "utt3", "seconds": 1.8, "text": "반가워요"},
    ]
    print("오늘 주제:", TOPIC)
    print(summarize_clips(clips))


if __name__ == "__main__":
    main()
