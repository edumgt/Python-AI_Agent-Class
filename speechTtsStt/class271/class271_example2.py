# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class271 example2: 음성 품질 평가 · 단계 2/7 기초 구현 [class271]"""

TOPIC = "음성 품질 평가 · 단계 2/7 기초 구현 [class271]"
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

def extension_mission():
    return {
        "mission": "snr 임계값을 조정해 noisy 판정 변화를 비교하세요.",
        "check": "짧은 발화/긴 발화를 분리해 전처리 전략을 달리 적용하세요.",
        "topic": TOPIC,
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("확장 미션:", extension_mission())
