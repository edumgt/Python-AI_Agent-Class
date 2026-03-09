# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class135 example1: NLP/STT/TTS 개요 · 단계 7/8 실전 검증 [class135]"""

TOPIC = "NLP/STT/TTS 개요 · 단계 7/8 실전 검증 [class135]"
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

if __name__ == "__main__":
    main()
