import google.generativeai as genai
from app.config import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")


def analyze_clip(transcript):

    prompt = f"""
    Analyze this VTuber clip.

    Transcript:
    {transcript}

    Return:
    - Viral score
    - Funny moments
    - Meme suggestions
    - Subtitle emphasis timing
    """

    response = model.generate_content(prompt)

    return response.text

import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash") # 속도를 위해 flash 모델 권장

def check_music_copyright(bgm_name, platform="YouTube"):
    prompt = f"""
    음원/BGM 이름: {bgm_name}
    플랫폼: {platform}
    
    위 음원이 해당 플랫폼의 저작권 가이드라인(Content ID 등)에 안전한지 분석해줘.
    1. 사용 가능 여부 (Yes/No/Caution)
    2. 수익 창출 가능 여부
    3. 출처 표기 필요 여부
    결론은 아주 짧고 명확하게 한국어로 답변해줘.
    """
    response = model.generate_content(prompt)
    return response.text
