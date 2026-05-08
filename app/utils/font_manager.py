from pathlib import Path

import requests


def ensure_fonts():
    font_dir = Path("app/assets/fonts")
    font_path = font_dir / "NanumGothic-Bold.ttf"
    font_dir.mkdir(parents=True, exist_ok=True)

    if not font_path.exists() or font_path.stat().st_size == 0:
        print("Font not found. Downloading NanumGothic from Google Fonts...")
        url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        font_path.write_bytes(response.content)
        print("Font downloaded successfully.")

    return str(font_path)

