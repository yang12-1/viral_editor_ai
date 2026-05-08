import whisper

model = whisper.load_model("medium")


def transcribe_video(video_path):
    result = model.transcribe(video_path)

    subtitles = []

    for segment in result["segments"]:
        subtitles.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        })

    return subtitles