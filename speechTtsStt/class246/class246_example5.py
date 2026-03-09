# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class246 example5: STT 전처리/학습 · 단계 2/6 기초 구현 [class246]"""

TOPIC = "STT 전처리/학습 · 단계 2/6 기초 구현 [class246]"
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

def ops_readiness_check():
    return {
        "risk": "실시간 처리 지연 임계치와 경보 조건을 정의하세요.",
        "monitoring": "핵심 지표를 1분 주기로 기록",
        "rollback": "문제 발생 시 이전 안정 버전으로 즉시 복귀",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("운영 준비 점검:", ops_readiness_check())
