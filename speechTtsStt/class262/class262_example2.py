# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class262 example2: 발화/화자 특성 이해"""

TOPIC = "발화/화자 특성 이해"
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


def extension_mission():
    return {
        "mission": "입력값을 바꿔 2가지 이상 결과를 비교하기",
        "check": "결과 차이를 한 줄로 설명하기",
    }

if __name__ == "__main__":
    main()
    print("확장 미션:", extension_mission())
