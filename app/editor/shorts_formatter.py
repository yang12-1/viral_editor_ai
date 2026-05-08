from moviepy.editor import *


def convert_to_vertical(clip):

    clip = clip.resize(height=1920)

    return clip.crop(
        x_center=clip.w / 2,
        width=1080,
        height=1920
    )
