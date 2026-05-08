import logging
import multiprocessing
import os

from app.analyzer.emotion_detector import detect_energy_peaks
from app.analyzer.scene_detector import detect_scenes
from app.analyzer.whisper_transcriber import transcribe_video
from app.downloader.youtube_downloader import download_youtube_video
from app.editor.auto_cut import create_highlight
from app.editor.ffmpeg_renderer import render_shorts_with_subs
from app.editor.meme_inserter import insert_meme_sfx_at_peaks
from app.editor.shorts_formatter import convert_to_vertical
from app.editor.subtitle_renderer import generate_ass_file
from app.editor.thumbnail_extractor import extract_hook_frame
from app.editor.zoom_effect import apply_zoom_effect
from app.llm.gemini_agent import check_music_copyright
from app.utils.asset_downloader import ensure_assets
from app.utils.font_manager import ensure_fonts


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()],
)


def run_pipeline():
    os.makedirs("output", exist_ok=True)

    logging.info("Step 0: Preparing environment and assets...")
    ensure_assets()
    font_path = ensure_fonts()
    logging.info("Font ready: %s", font_path)

    youtube_url = input("YouTube URL: ")
    logging.info("Step 1: Downloading YouTube video...")
    video_path = download_youtube_video(youtube_url)
    logging.info("Download complete: %s", video_path)

    logging.info("Step 2: Starting parallel analysis: scene detection + Whisper...")
    with multiprocessing.Pool(processes=2) as pool:
        scene_task = pool.apply_async(detect_scenes, (video_path,))
        whisper_task = pool.apply_async(transcribe_video, (video_path,))

        scenes = scene_task.get()
        subtitles = whisper_task.get()

    logging.info("Analysis finished. Found %s scenes and %s subtitle segments.", len(scenes), len(subtitles))

    logging.info("Step 2.5: Detecting high-energy reaction peaks for SFX...")
    energy_peaks = detect_energy_peaks(video_path)
    logging.info("Detected %s SFX candidate peaks.", len(energy_peaks))

    logging.info("Step 3: Checking copyright risk for recommended BGM...")
    bgm_suggestion = "Kawaii Future Bass"
    copyright_report = check_music_copyright(bgm_suggestion)
    logging.info("Copyright report: %s", copyright_report)

    logging.info("Step 4: Auto editing, vertical formatting, zoom and SFX...")
    clip = create_highlight(video_path, scenes)
    clip = apply_zoom_effect(clip)
    clip = convert_to_vertical(clip)
    clip = insert_meme_sfx_at_peaks(clip, energy_peaks, emotion="high")

    logging.info("Step 5: Generating dynamic ASS subtitles...")
    ass_path = "output/subtitles.ass"
    generate_ass_file(subtitles, ass_path)

    temp_output = "output/temp_no_subs.mp4"
    logging.info("Step 6: Rendering base video with MoviePy...")
    clip.write_videofile(
        temp_output,
        codec="libx264",
        audio_codec="aac",
        fps=60,
    )

    final_output = "output/final_shorts.mp4"
    logging.info("Step 7: Final rendering with FFmpeg subtitles...")
    render_shorts_with_subs(temp_output, final_output, ass_path)

    logging.info("Step 8: Extracting high-CTR hook thumbnail frame...")
    thumbnail = extract_hook_frame(final_output, "output/hook_thumbnail.jpg")
    logging.info("Hook thumbnail saved: %s", thumbnail)

    logging.info("=== Pipeline completed successfully! ===")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_pipeline()
