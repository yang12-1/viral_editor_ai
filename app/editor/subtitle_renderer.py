import datetime
import re


DEFAULT_HIGHLIGHT_KEYWORDS = [
    "미쳤",
    "레전드",
    "비상",
    "잠깐",
    "뭐야",
    "아니",
    "진짜",
    "대박",
    "웃겨",
    "소름",
    "왜",
]


def format_time(seconds):
    """Convert seconds to ASS timestamp format: H:MM:SS.cs."""
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    centiseconds = int(td.microseconds / 10000)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"


def _escape_ass(text):
    return str(text).replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", " ")


def _highlight_keywords(text, keywords=None):
    keywords = keywords or DEFAULT_HIGHLIGHT_KEYWORDS
    escaped_text = _escape_ass(text)

    for keyword in sorted(keywords, key=len, reverse=True):
        if not keyword:
            continue
        escaped_text = re.sub(
            re.escape(keyword),
            lambda match: r"{\c&H00FFFF&\fs92\b1}" + match.group(0) + r"{\rDefault}",
            escaped_text,
            flags=re.IGNORECASE,
        )

    return escaped_text


def generate_ass_file(subtitles, output_ass_path, highlight_keywords=None):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Alignment, MarginL, MarginR, MarginV, Outline, Shadow
Style: Default,NanumGothic,70,&H00FFFFFF,&H0000FFFF,&H00000000,&HAA000000,1,2,60,60,160,5,2
Style: Impact,NanumGothic,84,&H0000FFFF,&H0000FFFF,&H00000000,&HAA000000,1,2,60,60,170,6,3

[Events]
Format: Layer, Start, End, Style, Name, Text
"""

    with open(output_ass_path, "w", encoding="utf-8") as file:
        file.write(header)
        for sub in subtitles:
            start_t = format_time(sub["start"])
            end_t = format_time(sub["end"])
            duration = max(0.01, float(sub["end"]) - float(sub["start"]))
            pop_ms = min(180, int(duration * 1000 * 0.25))
            text = _highlight_keywords(sub["text"], highlight_keywords)
            animated_text = (
                r"{\fad(60,80)\t(0,"
                + str(pop_ms)
                + r",\fscx112\fscy112)\t("
                + str(pop_ms)
                + r","
                + str(pop_ms + 140)
                + r",\fscx100\fscy100)}"
                + text
            )
            file.write(f"Dialogue: 0,{start_t},{end_t},Default,,{animated_text}\n")

    print(f"ASS subtitle file generated: {output_ass_path}")
