from google.colab import userdata

# API Keys
OPENAI_API_KEY = userdata.get("OPENAI_API_KEY")
GEMINI_API_KEY = userdata.get("GEMINI_API_KEY")

# Video Settings
TARGET_RESOLUTION = (1080, 1920)
FPS = 60

# Clip Settings
MIN_CLIP_DURATION = 15
MAX_CLIP_DURATION = 45

# Whisper
WHISPER_MODEL = "medium"

# Rendering
VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"

# AI
OPENAI_MODEL = "gpt-4.1-mini"