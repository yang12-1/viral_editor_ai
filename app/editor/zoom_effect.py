from moviepy.editor import *


def apply_zoom_effect(clip):

    zoomed = clip.resize(
        lambda t: 1 + 0.03 * t
    )

    return zoomed
