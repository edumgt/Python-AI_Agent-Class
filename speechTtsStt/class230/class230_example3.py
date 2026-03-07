# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class230 example3: 음성 AI 개요"""

TOPIC = "음성 AI 개요"
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


def self_check():
    return [
        "입력/출력 형식을 다시 설명할 수 있는가?",
        "오류 상황 1가지를 직접 만들어 테스트했는가?",
        "핵심 로직을 함수 단위로 분리했는가?",
    ]

def challenge_case():
    return {
        "task": "같은 로직을 새로운 입력 데이터로 재실행",
        "goal": "결과 차이를 한 문장으로 요약",
    }

if __name__ == "__main__":
    main()
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
