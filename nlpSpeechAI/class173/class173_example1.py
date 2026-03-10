# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다

"""class173 example1: 음성 데이터 구조 이해 · 단계 5/8 응용 확장 [class173]"""

TOPIC = "음성 데이터 구조 이해 · 단계 5/8 응용 확장 [class173]"
EXAMPLE_TEMPLATE = "speech"
EXAMPLE_VARIANT = 1

import math

def resolve_mode():
    if "음성 데이터 구조 이해" in TOPIC:
        return "understanding"
    if "오디오 전처리" in TOPIC:
        return "preprocess"
    if "특징 추출" in TOPIC:
        return "model"
    if "NLP/STT/TTS 개요" in TOPIC:
        return "overview"
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
    if mode == "understanding":
        return {
            "speech_concepts": ["샘플링/주파수/진폭", "오디오 포맷(wav/mp3/flac)", "라벨/메타데이터 구조"],
            "format_count": report["format_count"],
            "speaker_count": report["speaker_count"],
        }
    if mode == "preprocess":
        return {
            "pipeline": ["파일 로딩", "구간 분할", "잡음 제거", "샘플레이트 변환", "Spectrogram/Mel"],
            "avg_sample_rate": report["avg_sample_rate"],
            "avg_seconds": report["avg_seconds"],
        }
    if mode == "model":
        return {
            "model_concepts": ["MFCC 특징", "음성 분류 기초", "ASR/TTS 구조"],
            "quality_distribution": {
                "clean": sum(1 for r in report["rows"] if r["quality"] == "clean"),
                "mid": sum(1 for r in report["rows"] if r["quality"] == "mid"),
                "noisy": sum(1 for r in report["rows"] if r["quality"] == "noisy"),
            },
            "service": service_blueprint(),
        }
    if mode == "overview":
        return {
            "overview": ["NLP + Speech 통합 흐름", "텍스트/음성 데이터 특성", "모델 개발 사이클"],
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

if __name__ == "__main__":
    main()
