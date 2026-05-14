from pathlib import Path

from moviepy.editor import *

MEME_SFX = {
    "high": "app/assets/sfx/vine_boom.mp3",
    "awkward": "app/assets/sfx/metal_pipe.mp3"
}


def insert_meme_sfx(clip, emotion):

    if emotion not in MEME_SFX:
        return clip

    sfx = AudioFileClip(MEME_SFX[emotion])

    final_audio = CompositeAudioClip([
        clip.audio,
        sfx.set_start(0)
    ])

    return clip.set_audio(final_audio)


def insert_meme_sfx_at_peaks(clip, peaks, emotion="high", max_insertions=8):
    sfx_path = Path(MEME_SFX.get(emotion, ""))
    if not sfx_path.exists() or not peaks:
        return clip

    layers = [clip.audio] if clip.audio is not None else []

    for peak in peaks[:max_insertions]:
        start = max(0.0, float(peak.get("time", 0.0)))
        if start > clip.duration:
            continue
        layers.append(AudioFileClip(str(sfx_path)).volumex(0.65).set_start(start))

    if not layers:
        return clip

    return clip.set_audio(CompositeAudioClip(layers))
