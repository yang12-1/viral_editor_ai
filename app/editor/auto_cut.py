from moviepy.editor import *


def create_highlight(video_path, scenes):
    base_clip = VideoFileClip(video_path)

    clips = []

    for scene in scenes:
        start = scene["start"]
        end = scene["end"]

        duration = end - start

        if duration < 1:
            continue

        clip = base_clip.subclip(start, end)

        clips.append(clip)

    final_clip = concatenate_videoclips(clips)

    return final_clip
