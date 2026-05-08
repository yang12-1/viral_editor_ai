import yt_dlp
import os

def download_youtube_video(url):

    os.makedirs("input", exist_ok=True)

    output_path = "input/video.mp4"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": output_path,
        "quiet": False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path
