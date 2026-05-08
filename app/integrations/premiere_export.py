import json


def export_premiere_timeline(clips):

    timeline = {
        "clips": clips
    }

    with open("output/premiere_timeline.json", "w") as f:
        json.dump(timeline, f, indent=4)
