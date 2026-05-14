import whisper

# 'medium' 모델은 정확하지만 무거우므로 성능과 타협 시 'small' 권장
model = whisper.load_model("small")

def transcribe_video_with_words(video_path):
    # word_timestamps를 True로 설정하여 단어별 시작/종료 시간 획득
    result = model.transcribe(video_path, word_timestamps=True)
    
    segments = []
    for segment in result["segments"]:
        segments.append({
            "text": segment["text"],
            "start": segment["start"],
            "end": segment["end"],
            "words": segment["words"] # 각 단어의 위치 정보 포함
        })
    return segments


def transcribe_video(video_path):
    return transcribe_video_with_words(video_path)
