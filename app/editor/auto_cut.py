from moviepy.editor import VideoFileClip, concatenate_videoclips


def create_highlight(video_path, scenes, target_duration=45, min_scene_duration=1.0):
    """Create a short highlight assembly from detected scenes.

    Current ranking is duration-based because the project does not yet merge
    transcript/chat/emotion scores into scene objects. The function is written
    to accept future scene["viral_score"] values without another API change.
    """
    base_clip = VideoFileClip(video_path)

    if not scenes:
        end = min(base_clip.duration, target_duration)
        return base_clip.subclip(0, end)

    ranked_scenes = sorted(
        scenes,
        key=lambda scene: scene.get("viral_score", min(scene["end"] - scene["start"], 8)),
        reverse=True,
    )

    clips = []
    total_duration = 0.0

    for scene in ranked_scenes:
        start = max(0.0, float(scene["start"]))
        end = min(float(scene["end"]), base_clip.duration)
        duration = end - start

        if duration < min_scene_duration:
            continue

        remaining = target_duration - total_duration
        if remaining <= 0:
            break

        if duration > remaining:
            end = start + remaining
            duration = remaining

        clips.append(base_clip.subclip(start, end))
        total_duration += duration

    if not clips:
        return base_clip.subclip(0, min(base_clip.duration, target_duration))

    return concatenate_videoclips(clips)
