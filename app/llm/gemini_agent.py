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
