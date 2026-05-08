import subprocess


def render_shorts(input_path, output_path):

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vf",
        "scale=1080:1920",
        "-r",
        "60",
        "-preset",
        "fast",
        output_path
    ]

    subprocess.run(cmd)