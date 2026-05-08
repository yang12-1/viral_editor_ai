import json


def export_resolve_timeline(clips):

    timeline = {
        "resolve_clips": clips
    }

    with open("output/resolve_timeline.json", "w") as f:
        json.dump(timeline, f, indent=4)