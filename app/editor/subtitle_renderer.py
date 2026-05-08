import datetime

def format_time(seconds):
    """초 단위 시간을 ASS 포맷(H:MM:SS.cs)으로 변환"""
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    centiseconds = int(td.microseconds / 10000)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"

def generate_ass_file(subtitles, output_ass_path):
    # 자막 스타일 설정 (글꼴, 크기, 색상 등)
    # &H0000FFFF: 노란색, &H00FFFFFF: 흰색 (순서는 ABGR)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, Bold, Alignment
Style: Default,NanumGothic,70,&H00FFFFFF,&H00000000,1,2
Style: Highlight,NanumGothic,80,&H0000FFFF,&H00000000,1,2

[Events]
Format: Layer, Start, End, Style, Name, Text
"""
    
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for sub in subtitles:
            start_t = format_time(sub["start"])
            end_t = format_time(sub["end"])
            # 기본 자막 출력
            f.write(f"Dialogue: 0,{start_t},{end_t},Default,,{sub['text']}\n")
            
    print(f"ASS subtitle file generated: {output_ass_path}")
