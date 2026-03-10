# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class246 example4: STT 전처리/학습 · 단계 2/6 기초 구현 [class246]"""

TOPIC = "STT 전처리/학습 · 단계 2/6 기초 구현 [class246]"
EXAMPLE_TEMPLATE = "speech"
EXAMPLE_VARIANT = 4

import math

def resolve_mode():
    if any(k in TOPIC for k in ["NLP/STT/TTS 개요", "음성 AI 개요"]):
        return "overview"
    if any(k in TOPIC for k in ["STT 파이프라인", "STT 데이터 라벨링", "발화/화자 특성 이해", "음성 데이터 구조 이해"]):
        return "data_prep"
    if any(k in TOPIC for k in ["오디오 전처리", "STT 전처리/학습"]):
        return "preprocess"
    if any(k in TOPIC for k in ["특징 추출", "음성 품질 평가"]):
        return "feature_model"
    if any(k in TOPIC for k in ["TTS 파이프라인", "TTS 전처리/학습"]):
        return "tts_model"
    if "모델 추론 및 튜닝" in TOPIC:
        return "tuning"
    if "실전 음성 모델 데모" in TOPIC:
        return "practice_demo"
    return "speech_general"

def build_test_cases():
    rows = [
        {
            "id": "utt1",
            "format": "wav",
            "sample_rate": 16000,
            "seconds": 1.2,
            "freq_hz": 220,
            "amplitude": 0.8,
            "snr_db": 22.4,
            "label": "hello ai",
            "speaker": "spk_a",
        },
        {
            "id": "utt2",
            "format": "mp3",
            "sample_rate": 22050,
            "seconds": 1.8,
            "freq_hz": 330,
            "amplitude": 0.6,
            "snr_db": 14.1,
            "label": "speech demo",
            "speaker": "spk_b",
        },
    ]
    if EXAMPLE_VARIANT >= 2:
        rows.append(
            {
                "id": "utt3",
                "format": "wav",
                "sample_rate": 8000,
                "seconds": 2.2,
                "freq_hz": 180,
                "amplitude": 0.7,
                "snr_db": 10.2,
                "label": "noisy sample",
                "speaker": "spk_a",
            }
        )
    if EXAMPLE_VARIANT >= 3:
        rows.append(
            {
                "id": "utt4",
                "format": "wav",
                "sample_rate": 44100,
                "seconds": 0.7,
                "freq_hz": 410,
                "amplitude": 0.9,
                "snr_db": 18.0,
                "label": "short clip",
                "speaker": "spk_c",
            }
        )
    if EXAMPLE_VARIANT >= 4:
        rows.append(
            {
                "id": "utt5",
                "format": "flac",
                "sample_rate": 16000,
                "seconds": 2.6,
                "freq_hz": 260,
                "amplitude": 0.5,
                "snr_db": 12.5,
                "label": "tts target",
                "speaker": "spk_d",
            }
        )
    if EXAMPLE_VARIANT >= 5:
        rows.append(
            {
                "id": "utt6",
                "format": "wav",
                "sample_rate": 12000,
                "seconds": 3.1,
                "freq_hz": 140,
                "amplitude": 0.4,
                "snr_db": 8.8,
                "label": "edge noisy",
                "speaker": "spk_e",
            }
        )
    return rows

def generate_wave(sample_rate, seconds, freq_hz, amplitude):
    size = max(16, int(sample_rate * min(seconds, 0.2)))
    signal = []
    for i in range(size):
        t = i / sample_rate
        v = amplitude * math.sin(2 * math.pi * freq_hz * t)
        signal.append(v)
    return signal

def segment_signal(signal, segment_size):
    chunks = []
    i = 0
    while i < len(signal):
        chunks.append(signal[i : i + segment_size])
        i += segment_size
    return chunks

def moving_average_denoise(signal, radius=1):
    out = []
    for i in range(len(signal)):
        start = max(0, i - radius)
        end = min(len(signal), i + radius + 1)
        win = signal[start:end]
        out.append(sum(win) / len(win))
    return out

def resample_linear(signal, src_rate, dst_rate):
    if src_rate == dst_rate or not signal:
        return list(signal)
    out_len = max(1, int(len(signal) * dst_rate / src_rate))
    out = []
    for i in range(out_len):
        pos = i * (len(signal) - 1) / max(1, out_len - 1)
        left = int(math.floor(pos))
        right = min(len(signal) - 1, left + 1)
        alpha = pos - left
        out.append(signal[left] * (1 - alpha) + signal[right] * alpha)
    return out

def spectrum_energy(signal, bins=16):
    if not signal:
        return [0.0] * bins
    chunk = max(1, len(signal) // bins)
    out = []
    for i in range(bins):
        seg = signal[i * chunk : (i + 1) * chunk]
        if not seg:
            out.append(0.0)
        else:
            out.append(sum(abs(v) for v in seg) / len(seg))
    return out

def mel_scale(freq_hz):
    return 2595.0 * math.log10(1.0 + freq_hz / 700.0)

def mel_bins(sample_rate, bins=8):
    nyq = sample_rate / 2.0
    step = nyq / bins
    return [round(mel_scale((i + 1) * step), 2) for i in range(bins)]

def mfcc_like(energies):
    if not energies:
        return []
    return [round(math.log(e + 1e-6), 4) for e in energies[:13]]

def classify_speech_quality(snr_db):
    if snr_db >= 20:
        return "clean"
    if snr_db >= 12:
        return "mid"
    return "noisy"

def asr_stub(text):
    return text.upper()

def tts_stub(text, sample_rate):
    return {"chars": len(text), "target_sr": sample_rate, "voice": "korean-neutral"}

def ctc_align_stub(text):
    # CTC 개념 데모: 반복 문자 병합 + blank 제거를 단순화해 표현
    collapsed = []
    prev = None
    for ch in text:
        if ch == "_":
            prev = ch
            continue
        if ch != prev:
            collapsed.append(ch)
        prev = ch
    return "".join(collapsed)

def whisper_stub(text):
    # Whisper 계열 동작 개념 데모(실제 모델 추론 아님)
    return {"transcript": text.lower(), "confidence": round(0.78 + EXAMPLE_VARIANT * 0.03, 3)}

def g2p_stub(text):
    # 한국어 발음열 변환의 축약 데모
    normalized = text.replace(" ", "")
    return [ch for ch in normalized if ch.strip()]

def tts_model_cards():
    return [
        {"name": "Tacotron", "strength": "자연스러운 멜 예측", "weakness": "추론 속도"},
        {"name": "FastSpeech", "strength": "빠른 추론", "weakness": "프로소디 제어 난이도"},
        {"name": "VITS", "strength": "고품질 end-to-end", "weakness": "학습 안정성 관리"},
    ]

def service_blueprint():
    return {
        "ingest": "audio upload / stream",
        "preprocess": "resample + denoise + segment",
        "features": "spectrogram + mel + mfcc",
        "model": "ASR or TTS or classification",
        "serving": "API + monitoring + metadata logging",
    }

def analyze_rows():
    rows = build_test_cases()
    analyzed = []
    format_count = {}
    speaker_count = {}
    for row in rows:
        signal = generate_wave(row["sample_rate"], row["seconds"], row["freq_hz"], row["amplitude"])
        seg_size = max(8, len(signal) // 4)
        segments = segment_signal(signal, seg_size)
        denoised = moving_average_denoise(signal, radius=1)
        resampled = resample_linear(denoised, row["sample_rate"], 16000)
        spec = spectrum_energy(resampled, bins=16)
        mel = mel_bins(16000, bins=8)
        mfcc = mfcc_like(spec)
        quality = classify_speech_quality(row["snr_db"])
        analyzed_row = {
            "id": row["id"],
            "format": row["format"],
            "sample_rate": row["sample_rate"],
            "seconds": row["seconds"],
            "label": row["label"],
            "speaker": row["speaker"],
            "segments": len(segments),
            "quality": quality,
            "spectrogram_bins": len(spec),
            "mel_bins": mel[:4],
            "mfcc_head": mfcc[:5],
            "asr_text": asr_stub(row["label"]),
            "tts_meta": tts_stub(row["label"], 16000),
        }
        analyzed.append(analyzed_row)
        format_count[row["format"]] = format_count.get(row["format"], 0) + 1
        speaker_count[row["speaker"]] = speaker_count.get(row["speaker"], 0) + 1
    return {
        "rows": analyzed,
        "format_count": format_count,
        "speaker_count": speaker_count,
        "avg_seconds": round(sum(r["seconds"] for r in rows) / len(rows), 3),
        "avg_sample_rate": int(sum(r["sample_rate"] for r in rows) / len(rows)),
    }

def build_mode_summary(mode, report):
    if mode == "overview":
        return {
            "stt_tts_concepts": ["STT(음성→텍스트)", "TTS(텍스트→음성)", "음성비서/콜센터/자막/낭독"],
            "service": service_blueprint(),
            "sample_count": len(report["rows"]),
        }
    if mode == "data_prep":
        return {
            "data_prep": ["음성 수집", "스크립트 정렬", "발화 단위 관리", "화자 정보 관리", "데이터 증강"],
            "format_count": report["format_count"],
            "speaker_count": report["speaker_count"],
        }
    if mode == "preprocess":
        return {
            "pipeline": ["파일 로딩", "구간 분할", "잡음 제거", "샘플레이트 변환", "Spectrogram/Mel"],
            "avg_sample_rate": report["avg_sample_rate"],
            "avg_seconds": report["avg_seconds"],
        }
    if mode == "feature_model":
        return {
            "feature_stack": ["waveform", "STFT", "Mel-Spectrogram", "MFCC", "발음-음향 특징 관계"],
            "quality_distribution": {
                "clean": sum(1 for r in report["rows"] if r["quality"] == "clean"),
                "mid": sum(1 for r in report["rows"] if r["quality"] == "mid"),
                "noisy": sum(1 for r in report["rows"] if r["quality"] == "noisy"),
            },
            "service": service_blueprint(),
        }
    if mode == "tts_model":
        return {
            "tts_flow": ["텍스트→발음열", "음향모델", "보코더"],
            "g2p_preview": g2p_stub("한국어 tts 실습"),
            "models": tts_model_cards(),
        }
    if mode == "tuning":
        ctc_preview = ctc_align_stub("hh__ee_ll_ll_oo")
        whisper_preview = whisper_stub("안녕하세요 STT 모델 테스트")
        return {
            "stt_model_concepts": ["음성→텍스트 구조", "음향모델/언어모델", "CTC", "Whisper", "한국어 STT 고려사항"],
            "ctc_demo": ctc_preview,
            "whisper_demo": whisper_preview,
            "korean_stt_checks": ["받침/연음", "외래어", "숫자/기호 읽기"],
        }
    if mode == "practice_demo":
        return {
            "stt_practice": ["오픈소스 STT 사용", "음성→텍스트 추출", "구간별 자막 생성", "STT 성능 확인"],
            "tts_practice": ["텍스트→음성 변환", "톤/속도 조절", "샘플 문장 낭독", "한국어 TTS 실습"],
            "service": service_blueprint(),
        }
    return {"avg_seconds": report["avg_seconds"], "formats": report["format_count"]}

def main():
    print("오늘 주제:", TOPIC)
    mode = resolve_mode()
    report = analyze_rows()
    summary = build_mode_summary(mode, report)
    print("모드:", mode)
    print("요약:", summary)
    return {
        "variant": EXAMPLE_VARIANT,
        "mode": mode,
        "sample_count": len(report["rows"]),
        "summary": summary,
    }

def mini_project_plan():
    return {
        "scenario": "오디오 포맷(wav/mp3/flac)별 품질 리포트를 CSV로 내보내세요.",
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
