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