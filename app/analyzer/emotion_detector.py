import librosa
import numpy as np


def detect_emotion(audio_path):
    y, sr = librosa.load(audio_path)

    rms = librosa.feature.rms(y=y)[0]

    energy = np.mean(rms)

    if energy > 0.1:
        return {
            "emotion": "high",
            "score": float(energy)
        }

    return {
        "emotion": "normal",
        "score": float(energy)
    }


def detect_energy_peaks(audio_path, threshold_percentile=88, min_interval=1.2, lead_time=0.1):
    """Return high-energy timestamps for impact SFX insertion.

    The timestamp is shifted slightly earlier so the impact sound lands just
    before the streamer reaction peak.
    """
    y, sr = librosa.load(audio_path, mono=True)
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)

    if len(rms) == 0:
        return []

    threshold = np.percentile(rms, threshold_percentile)
    peaks = []
    last_time = -min_interval

    for idx in range(1, len(rms) - 1):
        is_peak = rms[idx] >= threshold and rms[idx] >= rms[idx - 1] and rms[idx] >= rms[idx + 1]
        if not is_peak:
            continue

        timestamp = max(0.0, float(times[idx] - lead_time))
        if timestamp - last_time < min_interval:
            continue

        peaks.append({
            "time": timestamp,
            "score": float(rms[idx]),
            "emotion": "high"
        })
        last_time = timestamp

    return peaks
