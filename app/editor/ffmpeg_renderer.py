import subprocess
from pathlib import Path


def _ass_filter_path(path):
    return path.replace("\\", "/").replace(":", "\\:")


def render_shorts_with_subs(input_path, output_path, ass_path, fonts_dir="app/assets/fonts"):
    safe_ass_path = _ass_filter_path(ass_path)
    safe_fonts_dir = _ass_filter_path(str(Path(fonts_dir)))
    vf = f"ass={safe_ass_path}:fontsdir={safe_fonts_dir},scale=1080:1920"

    nvenc_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-vf",
        vf,
        "-c:v",
        "h264_nvenc",
        "-preset",
        "fast",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        output_path,
    ]

    result = subprocess.run(nvenc_cmd)
    if result.returncode == 0:
        return

    print("[ffmpeg] h264_nvenc failed. Retrying with libx264 CPU encoder...")
    cpu_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        output_path,
    ]
    subprocess.run(cpu_cmd, check=True)

def normalize_video_for_editing(input_path, output_path="input/video_normalized.mp4"):
    """Transcode to Colab-friendly H.264/AAC for OpenCV, MoviePy, and PySceneDetect."""
    output_path = str(output_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-map",
        "0:v:0",
        "-map",
        "0:a:0?",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        output_path,
    ]
    subprocess.run(cmd, check=True)
    return output_path
