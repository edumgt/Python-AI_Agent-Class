# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class170 example3: 음성 데이터 구조 이해 · 단계 2/8 기초 구현 [class170]"""

TOPIC = "음성 데이터 구조 이해 · 단계 2/8 기초 구현 [class170]"
EXAMPLE_TEMPLATE = "speech"

def summarize_utterances(rows):
    avg_seconds = sum(r["seconds"] for r in rows) / len(rows)
    noise_flags = [r["id"] for r in rows if r["snr_db"] < 12]
    return {
        "count": len(rows),
        "avg_seconds": round(avg_seconds, 2),
        "noisy_ids": noise_flags,
    }

def main():
    print("오늘 주제:", TOPIC)
    rows = [
        {"id": "utt1", "seconds": 1.8, "snr_db": 15.2},
        {"id": "utt2", "seconds": 2.9, "snr_db": 10.5},
        {"id": "utt3", "seconds": 1.1, "snr_db": 18.7},
    ]
    report = summarize_utterances(rows)
    print("음성 품질 요약:", report)
    return report

def self_check():
    return [
        "입력/출력 스키마를 문장으로 설명할 수 있는가?",
        "예외 입력을 최소 1개 이상 테스트했는가?",
        "결과를 재현 가능한 형태로 로그에 남겼는가?",
    ]

def challenge_case():
    return {
        "task": "STT 오류가 많은 구간을 규칙 기반으로 탐지하세요.",
        "goal": "핵심 변화 포인트를 3줄 요약",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("자가 점검:", self_check())
    print("챌린지:", challenge_case())
