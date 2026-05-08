from scenedetect import detect, ContentDetector


def detect_scenes(video_path):
    scenes = detect(video_path, ContentDetector())

    results = []

    for scene in scenes:
        start = scene[0].get_seconds()
        end = scene[1].get_seconds()

        results.append({
            "start": start,
            "end": end
        })

    return results
