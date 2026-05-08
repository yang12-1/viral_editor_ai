# VTuber Viral Editor AI

AI-powered automatic VTuber short-form editing system.

## Features
- Whisper transcription
- YOLO face tracking
- Meme insertion
- FFmpeg rendering
- Viral score prediction
- TikTok/Reels optimization
- Hook thumbnail extraction
- Keyword-highlighted ASS subtitles
- Audio energy peak based SFX timing
- Manifest-based asset downloading

## Installation

pip install -r requirements.txt

## Run

python app/main.py

## Google Colab Quickstart

```python
!git clone https://github.com/yang12-1/viral_editor_ai.git
%cd viral_editor_ai
!apt-get -qq update
!apt-get -qq install -y ffmpeg fontconfig
!pip -q install -r requirements.txt
```

```python
YOUTUBE_URL = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
!python -m app.colab_runner --youtube-url "$YOUTUBE_URL" --target-duration 45 --max-sfx 8
```

If you uploaded a local video to Colab instead:

```python
VIDEO_PATH = "/content/input.mp4"
!python -m app.colab_runner --video-path "$VIDEO_PATH" --target-duration 45 --max-sfx 8
```

Generated files:

- `output/final_shorts.mp4`
- `output/hook_thumbnail.jpg`
- `output/subtitles.ass`
- `output/colab_result.json`

## Assets

`app/assets/asset_manifest.json` defines downloadable assets. Fonts are downloaded
automatically. For meme SFX/BGM, set direct URLs that you have rights to use:

```bash
set VINE_BOOM_URL=https://example.com/vine_boom.mp3
set METAL_PIPE_URL=https://example.com/metal_pipe.mp3
```

Then run the pipeline. Assets are saved under `app/assets/sfx`, `app/assets/bgm`,
`app/assets/fonts`, and `app/assets/memes`.
