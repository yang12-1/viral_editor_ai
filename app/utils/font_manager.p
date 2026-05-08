import os
import requests

def ensure_fonts():
    font_dir = "app/assets/fonts"
    font_path = os.path.join(font_dir, "NanumGothic-Bold.ttf")
    
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
        
    if not os.path.exists(font_path):
        print("Font not found. Downloading NanumGothic from Google Fonts...")
        # 나눔고딕 볼드 직접 다운로드 링크 (예시)
        url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf"
        response = requests.get(url)
        with open(font_path, "wb") as f:
            f.write(response.content)
        print("Font downloaded successfully.")
    
    return font_path
