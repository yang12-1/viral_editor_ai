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

## Assets

`app/assets/asset_manifest.json` defines downloadable assets. Fonts are downloaded
automatically. For meme SFX/BGM, set direct URLs that you have rights to use:

```bash
set VINE_BOOM_URL=https://example.com/vine_boom.mp3
set METAL_PIPE_URL=https://example.com/metal_pipe.mp3
```

Then run the pipeline. Assets are saved under `app/assets/sfx`, `app/assets/bgm`,
`app/assets/fonts`, and `app/assets/memes`.
