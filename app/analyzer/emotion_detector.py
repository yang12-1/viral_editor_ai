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
