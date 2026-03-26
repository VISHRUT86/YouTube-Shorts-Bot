import os
import unicodedata

def clean_hindi_text(text):
    return unicodedata.normalize('NFC', text)

def get_audio_duration(audio_path):
    """Get exact audio duration in seconds using FFprobe."""
    import subprocess
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        print(f"[Subtitles] Audio duration: {duration:.2f}s")
        return duration
    except Exception as e:
        print(f"[Subtitles] Could not get duration: {e}")
        return None

def text_to_srt(full_script, duration_seconds, output_path, audio_path=None):
    """Generate perfectly synced subtitles using actual audio duration."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    full_script = clean_hindi_text(full_script)

    # Use actual audio duration for perfect sync
    if audio_path and os.path.exists(audio_path):
        actual_duration = get_audio_duration(audio_path)
        if actual_duration:
            duration_seconds = actual_duration
            print(f"[Subtitles] Syncing to actual audio: {duration_seconds:.2f}s")

    words = full_script.split()
    total_words = len(words)

    # 3 words per chunk for Hindi
    chunk_size = 3
    chunks = []
    for i in range(0, total_words, chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

    time_per_chunk = duration_seconds / max(len(chunks), 1)

    srt_lines = []
    for idx, chunk in enumerate(chunks):
        start_s = idx * time_per_chunk
        end_s   = (idx + 1) * time_per_chunk - 0.1

        srt_lines.append(f"{idx + 1}")
        srt_lines.append(f"{_srt_time(start_s)} --> {_srt_time(end_s)}")
        srt_lines.append(chunk)
        srt_lines.append("")

    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(srt_lines))

    print(f"[Subtitles] SRT saved: {len(chunks)} chunks")
    return output_path

def text_to_chunks(full_script, duration_seconds, audio_path=None):
    """Return timed chunks for Pillow-based subtitle rendering."""
    full_script = clean_hindi_text(full_script)

    if audio_path and os.path.exists(audio_path):
        actual = get_audio_duration(audio_path)
        if actual:
            duration_seconds = actual

    words = full_script.split()
    chunk_size = 3
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

    time_per_chunk = duration_seconds / max(len(chunks), 1)

    timed = []
    for idx, chunk in enumerate(chunks):
        timed.append({
            "text":  chunk,
            "start": idx * time_per_chunk,
            "end":   (idx + 1) * time_per_chunk - 0.1
        })
    return timed

def _srt_time(s):
    s = max(0, s)
    h  = int(s // 3600)
    m  = int((s % 3600) // 60)
    sc = int(s % 60)
    ms = int((s - int(s)) * 1000)
    return f"{h:02d}:{m:02d}:{sc:02d},{ms:03d}"