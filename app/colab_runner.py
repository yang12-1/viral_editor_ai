import argparse
import json
import os
from pathlib import Path

from app.analyzer.emotion_detector import detect_energy_peaks
from app.analyzer.scene_detector import detect_scenes
from app.analyzer.whisper_transcriber import transcribe_video
from app.downloader.youtube_downloader import download_youtube_video
from app.editor.auto_cut import create_highlight
from app.editor.ffmpeg_renderer import normalize_video_for_editing, render_shorts_with_subs
from app.editor.meme_inserter import insert_meme_sfx_at_peaks
from app.editor.shorts_formatter import convert_to_vertical
from app.editor.subtitle_renderer import generate_ass_file
from app.editor.thumbnail_extractor import extract_hook_frame
from app.editor.zoom_effect import apply_zoom_effect
from app.utils.asset_downloader import ensure_assets
from app.utils.font_manager import ensure_fonts


def _resolve_input_video(youtube_url=None, video_path=None):
    if youtube_url:
        return download_youtube_video(youtube_url)

    if video_path:
        candidate = Path(video_path)
        if not candidate.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        return str(candidate)

    raise ValueError("Set either --youtube-url or --video-path.")


def run_colab_pipeline(
    youtube_url=None,
    video_path=None,
    output_dir="output",
    target_duration=45,
    max_sfx=8,
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ensure_assets()
    ensure_fonts()

    source_video = _resolve_input_video(youtube_url=youtube_url, video_path=video_path)
    print(f"[1/8] Source video: {source_video}")

    print("[1.5/8] Normalizing video to H.264/AAC for Colab decoding...")
    source_video = normalize_video_for_editing(source_video, str(output_dir / "source_normalized.mp4"))
    print(f"Normalized video: {source_video}")


    print("[2/8] Scene detection...")
    scenes = detect_scenes(source_video)

    if not scenes:
        print("[warn] Scene detection returned 0 scenes. Falling back to the first target-duration seconds.")
        scenes = [{"start": 0.0, "end": float(target_duration), "viral_score": 1.0}]
    print(f"Detected scenes: {len(scenes)}")

    print("[3/8] Whisper transcription...")
    subtitles = transcribe_video(source_video)
    print(f"Subtitle segments: {len(subtitles)}")

    print("[4/8] Audio energy peak detection...")
    energy_peaks = detect_energy_peaks(source_video)
    print(f"SFX candidates: {len(energy_peaks)}")

    print("[5/8] Highlight assembly + vertical format + zoom + SFX...")
    clip = create_highlight(source_video, scenes, target_duration=target_duration)
    clip = apply_zoom_effect(clip)
    clip = convert_to_vertical(clip)
    clip = insert_meme_sfx_at_peaks(clip, energy_peaks, emotion="high", max_insertions=max_sfx)

    ass_path = output_dir / "subtitles.ass"
    print("[6/8] Dynamic ASS subtitles...")
    generate_ass_file(subtitles, str(ass_path))

    temp_output = output_dir / "temp_no_subs.mp4"
    print("[7/8] MoviePy base render...")
    clip.write_videofile(
        str(temp_output),
        codec="libx264",
        audio_codec="aac",
        fps=60,
    )

    final_output = output_dir / "final_shorts.mp4"
    print("[8/8] FFmpeg final render + hook thumbnail...")
    render_shorts_with_subs(str(temp_output), str(final_output), str(ass_path))
    thumbnail = extract_hook_frame(str(final_output), str(output_dir / "hook_thumbnail.jpg"))

    result = {
        "source_video": source_video,
        "final_video": str(final_output),
        "thumbnail": thumbnail,
        "subtitles": str(ass_path),
        "scene_count": len(scenes),
        "subtitle_count": len(subtitles),
        "sfx_candidate_count": len(energy_peaks),
    }

    report_path = output_dir / "colab_result.json"
    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--youtube-url", default=os.getenv("YOUTUBE_URL"))
    parser.add_argument("--video-path", default=os.getenv("VIDEO_PATH"))
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--target-duration", type=float, default=45)
    parser.add_argument("--max-sfx", type=int, default=8)
    args = parser.parse_args()

    run_colab_pipeline(
        youtube_url=args.youtube_url,
        video_path=args.video_path,
        output_dir=args.output_dir,
        target_duration=args.target_duration,
        max_sfx=args.max_sfx,
    )


if __name__ == "__main__":
    main()
