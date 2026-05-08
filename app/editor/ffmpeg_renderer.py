import subprocess
import os

def render_shorts_with_subs(input_path, output_path, ass_path):
    # 윈도우 경로인 경우 역슬래시(\)를 슬래시(/)로 바꾸고 따옴표 처리를 해줘야 FFmpeg이 인식합니다.
    safe_ass_path = ass_path.replace("\\", "/").replace(":", "\\:")
    
    cmd = [
        "ffmpeg",
        "-y", # 기존 파일 덮어쓰기 허용
        "-i", input_path,
        "-vf", f"ass={safe_ass_path},scale=1080:1920", # 자막 입히고 스케일 조정
        "-c:v", "h264_nvenc", # GPU 가속 (NVIDIA 기준, 없으면 libx264)
        "-preset", "fast",
        output_path
    ]
    
    subprocess.run(cmd)
