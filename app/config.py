import os

# Google Colab 환경인지 확인하고 Secrets에서 키 가져오기
try:
    from google.colab import userdata
    OPENAI_API_KEY = userdata.get('OPENAI_API_KEY')
    PEXELS_API_KEY = userdata.get('PEXELS_API_KEY')
    ELEVENLABS_API_KEY = userdata.get('ELEVENLABS_API_KEY')
except ImportError:
    # 로컬 환경인 경우 .env 파일 또는 시스템 환경 변수 사용
    from dotenv import load_dotenv
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# 경로 설정
OUTPUT_DIR = "output"
TEMP_DIR = "temp"
ASSETS_DIR = "assets"

# 영상 설정
VIDEO_ASPECT_RATIO = (9, 16)
# Colab은 나눔고딕 등이 기본 설치되어 있지 않으므로 폰트 경로 주의
FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" 

# 폴더 생성 로직
for path in [OUTPUT_DIR, TEMP_DIR, ASSETS_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)
