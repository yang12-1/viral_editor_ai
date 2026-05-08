from moviepy.editor import *


def add_subtitles(video_clip, subtitles):

    subtitle_clips = []

    for sub in subtitles:

        txt = TextClip(
            sub["text"],
            fontsize=70,
            color="white",
            font="Arial-Bold"
        )

        txt = txt.set_position(("center", 1500))

        txt = txt.set_start(sub["start"])
        txt = txt.set_end(sub["end"])

        subtitle_clips.append(txt)

    final = CompositeVideoClip([
        video_clip,
        *subtitle_clips
    ])

    return final