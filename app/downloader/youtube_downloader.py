import yt_dlp
import os

def download_youtube_video(url):

    os.makedirs("input", exist_ok=True)

    output_path = "input/video.mp4"

    ydl_opts = {
        # Avoid AV1 formats in Colab because OpenCV/PySceneDetect often fail to
        # decode them. Prefer H.264 AVC video + M4A audio, then fall back to mp4.
        "format": (
            "bestvideo[vcodec^=avc1][ext=mp4]+bestaudio[ext=m4a]/"
            "bestvideo[vcodec^=h264][ext=mp4]+bestaudio[ext=m4a]/"
            "best[ext=mp4][vcodec^=avc1]/"
            "best[ext=mp4]/best"
        ),
        "merge_output_format": "mp4",
        "outtmpl": output_path,
        "quiet": False
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path
