# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class263 example4: 발화/화자 특성 이해 · 단계 7/7 운영 최적화 [class263]"""

TOPIC = "발화/화자 특성 이해 · 단계 7/7 운영 최적화 [class263]"
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

def mini_project_plan():
    return {
        "scenario": "발화 단위 품질 리포트를 CSV로 내보내세요.",
        "steps": [
            "1) baseline 실행",
            "2) 개선안 적용",
            "3) 지표/로그 비교",
        ],
        "done_when": "기준 대비 개선 근거가 숫자로 제시됨",
    }

if __name__ == "__main__":
    summary = main()
    print("요약:", summary)
    print("미니 프로젝트:", mini_project_plan())
