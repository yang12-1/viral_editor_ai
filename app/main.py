import os
import multiprocessing
import logging

# 기존 모듈들
from app.downloader.youtube_downloader import download_youtube_video
from app.analyzer.scene_detector import detect_scenes
from app.analyzer.whisper_transcriber import transcribe_video
from app.editor.auto_cut import create_highlight
from app.editor.zoom_effect import apply_zoom_effect
from app.editor.shorts_formatter import convert_to_vertical

# 새로 교체/추가된 모듈들
from app.utils.font_manager import ensure_fonts
from app.llm.gemini_agent import check_music_copyright
from app.editor.subtitle_renderer import generate_ass_file
from app.editor.ffmpeg_renderer import render_shorts_with_subs

# 로깅 설정 (콘솔 및 파일 저장)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()]
)

def run_pipeline():
    # 1. 환경 준비 및 폰트 체크
    logging.info("Step 0: Preparing environment...")
    font_path = ensure_fonts()
    
    # 2. YouTube 영상 다운로드
    YOUTUBE_URL = input("YouTube URL: ")
    logging.info("Step 1: Downloading YouTube Video...")
    VIDEO_PATH = download_youtube_video(YOUTUBE_URL)
    logging.info(f"Download Complete: {VIDEO_PATH}")

    # 3. 멀티 프로세싱을 이용한 병렬 분석 (Scene + Whisper)
    # CPU/GPU 리소스를 최대로 활용하여 분석 시간을 단축합니다.
    logging.info("Step 2: Starting Parallel Analysis (Scene + Whisper)...")
    
    with multiprocessing.Pool(processes=2) as pool:
        scene_task = pool.apply_async(detect_scenes, (VIDEO_PATH,))
        whisper_task = pool.apply_async(transcribe_video, (VIDEO_PATH,))
        
        scenes = scene_task.get()
        subtitles = whisper_task.get()

    logging.info(f"Analysis Finished. Found {len(scenes)} scenes.")

    # 4. 저작권 검토 (예시: 영상 분석 결과에 따른 BGM 추천 시)
    # 실제 구현 시 크롤러에서 가져온 곡명을 넣으시면 됩니다.
    logging.info("Step 3: Checking Copyright for Recommended BGM...")
    bgm_suggestion = "Kawaii Future Bass" 
    copyright_report = check_music_copyright(bgm_suggestion)
    logging.info(f"Copyright Report: {copyright_report}")

    # 5. MoviePy를 이용한 영상 편집 (컷, 줌, 세로 포맷)
    logging.info("Step 4: Auto Editing & Formatting...")
    clip = create_highlight(VIDEO_PATH, scenes)
    clip = apply_zoom_effect(clip)
    clip = convert_to_vertical(clip)

    # 6. 자막 파일(ASS) 생성
    logging.info("Step 5: Generating ASS Subtitle File...")
    ASS_PATH = "output/subtitles.ass"
    generate_ass_file(subtitles, ASS_PATH)

    # 7. MoviePy 1차 렌더링 (자막 제외한 순수 영상 조립)
    TEMP_OUTPUT = "output/temp_no_subs.mp4"
    if not os.path.exists("output"):
        os.makedirs("output")
        
    logging.info("Step 6: Rendering Base Video (MoviePy)...")
    clip.write_videofile(
        TEMP_OUTPUT,
        codec="libx264",
        audio_codec="aac",
        fps=60 # 쇼츠 최적화 프레임
    )

    # 8. FFmpeg 최종 렌더링 (자막 입히기 + 하드웨어 가속)
    FINAL_OUTPUT = "output/final_shorts.mp4"
    logging.info("Step 7: Final Rendering with Subtitles (FFmpeg)...")
    render_shorts_with_subs(TEMP_OUTPUT, FINAL_OUTPUT, ASS_PATH)

    logging.info("=== All Process Completed Successfully! ===")

if __name__ == "__main__":
    # 윈도우 환경에서 멀티 프로세싱 안정성을 위해 필수입니다.
    multiprocessing.freeze_support()
    run_pipeline()
