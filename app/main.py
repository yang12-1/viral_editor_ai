from app.analyzer.scene_detector import detect_scenes
from app.analyzer.whisper_transcriber import transcribe_video
from app.editor.auto_cut import create_highlight
from app.editor.subtitle_renderer import add_subtitles
from app.editor.zoom_effect import apply_zoom_effect
from app.editor.shorts_formatter import convert_to_vertical
from app.editor.ffmpeg_renderer import render_shorts

VIDEO_PATH = "input/video.mp4"

print("Scene Detection...")
scenes = detect_scenes(VIDEO_PATH)

print("Whisper Transcription...")
subtitles = transcribe_video(VIDEO_PATH)

print("Auto Editing...")
clip = create_highlight(VIDEO_PATH, scenes)

print("Zoom Effects...")
clip = apply_zoom_effect(clip)

print("Vertical Formatting...")
clip = convert_to_vertical(clip)

print("Subtitle Rendering...")
clip = add_subtitles(clip, subtitles)

TEMP_OUTPUT = "output/temp.mp4"
FINAL_OUTPUT = "output/final_shorts.mp4"


clip.write_videofile(TEMP_OUTPUT)

print("FFmpeg Rendering...")
render_shorts(TEMP_OUTPUT, FINAL_OUTPUT)

print("Completed")
