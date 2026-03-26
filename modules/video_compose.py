import subprocess
import os
import glob
import random
import shutil

from PIL import Image, ImageDraw, ImageFont
from config import VIDEO_WIDTH, VIDEO_HEIGHT, FPS

FONT_PATH = "assets/fonts/Hind-Bold.ttf"


def get_random_music():
    """Pick random music from assets/music folder."""
    music_files = glob.glob("assets/music/*.mp3")
    if not music_files:
        return None
    chosen = random.choice(music_files)
    print(f"[Music] Selected: {os.path.basename(chosen)}")
    return chosen

def burn_subtitles_pillow(image, text, font_size=65):
    """Burn Hindi subtitle with correct Unicode rendering."""
    import unicodedata

    img  = image.copy()
    draw = ImageDraw.Draw(img)

    # Normalize Hindi Unicode
    text = unicodedata.normalize('NFC', text)

    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except Exception as e:
        print(f"[Warning] Font error: {e}")
        font = ImageFont.load_default()

    text_x = VIDEO_WIDTH  // 2
    text_y = VIDEO_HEIGHT - 300

    # Word wrap if text too long
    max_width = VIDEO_WIDTH - 100
    words     = text.split()
    lines     = []
    current   = ""

    for word in words:
        test = (current + " " + word).strip()
        try:
            bbox = font.getbbox(test)
            w    = bbox[2] - bbox[0]
        except:
            w = len(test) * 30
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    # Draw each line
    line_height = font_size + 10
    total_h     = len(lines) * line_height
    start_y     = text_y - total_h // 2

    for i, line in enumerate(lines):
        ly = start_y + i * line_height

        # Semi-transparent background box
        try:
            bbox  = font.getbbox(line)
            lw    = bbox[2] - bbox[0]
            pad   = 20
            box_x1 = text_x - lw // 2 - pad
            box_y1 = ly - line_height // 2 - 5
            box_x2 = text_x + lw // 2 + pad
            box_y2 = ly + line_height // 2 + 5

            # Dark background for readability
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ov_draw = ImageDraw.Draw(overlay)
            ov_draw.rounded_rectangle(
                [box_x1, box_y1, box_x2, box_y2],
                radius=10,
                fill=(0, 0, 0, 160)
            )
            img = Image.alpha_composite(
                img.convert("RGBA"), overlay
            ).convert("RGB")
            draw = ImageDraw.Draw(img)
        except:
            pass

        # Outline
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx == 0 and dy == 0:
                    continue
                draw.text(
                    (text_x + dx, ly + dy),
                    line, font=font,
                    fill=(0, 0, 0), anchor="mm"
                )

        # Main white text
        draw.text(
            (text_x, ly),
            line, font=font,
            fill=(255, 255, 0),  # Yellow — easy to read
            anchor="mm"
        )

    return img


def compose_video(
    image_paths=None, audio_path=None, subtitle_path=None,
    output_path=None, duration=45, timed_chunks=None
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not image_paths:
        print("[Video] No images found.")
        return None

    frames_dir = output_path.replace(".mp4", "_frames")
    os.makedirs(frames_dir, exist_ok=True)

    # ── Audio duration ──────────────────────────────────
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ], capture_output=True, text=True)
        actual_duration = float(result.stdout.strip())
    except:
        actual_duration = duration

    total_frames   = int(actual_duration * FPS)
    frames_per_img = max(1, total_frames // len(image_paths))

    print(f"[Video] Duration: {actual_duration:.1f}s | Frames: {total_frames}")

    # ── Preload images ──────────────────────────────────
    images = [
        Image.open(p).convert("RGB").resize((VIDEO_WIDTH, VIDEO_HEIGHT))
        for p in image_paths
    ]

    # ── Frame generation ────────────────────────────────
    frame_idx = 0
    for img_i, base_img in enumerate(images):
        img_start = (img_i * frames_per_img) / FPS

        for f in range(frames_per_img):
            current_time = img_start + (f / FPS)
            current_text = ""

            if timed_chunks:
                for chunk in timed_chunks:
                    if chunk["start"] <= current_time < chunk["end"]:
                        current_text = chunk["text"]
                        break

            frame_img = (
                burn_subtitles_pillow(base_img, current_text)
                if current_text else base_img.copy()
            )

            frame_img.save(
                os.path.join(frames_dir, f"frame_{frame_idx:06d}.jpg"),
                quality=90
            )
            frame_idx += 1

    # Remaining frames with last image
    while frame_idx < total_frames:
        current_time = frame_idx / FPS
        current_text = ""
        if timed_chunks:
            for chunk in timed_chunks:
                if chunk["start"] <= current_time < chunk["end"]:
                    current_text = chunk["text"]
                    break

        frame_img = (
            burn_subtitles_pillow(images[-1], current_text)
            if current_text else images[-1].copy()
        )
        frame_img.save(
            os.path.join(frames_dir, f"frame_{frame_idx:06d}.jpg"),
            quality=90
        )
        frame_idx += 1

    print(f"[Video] Frames created: {frame_idx} ✅")

    # ── Combine frames into video ───────────────────────
    temp_video = output_path.replace(".mp4", "_temp.mp4")

    r1 = subprocess.run([
        "ffmpeg", "-y",
        "-v", "quiet", "-stats",
        "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%06d.jpg"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        temp_video
    ], capture_output=True, text=True)

    if r1.returncode != 0:
        print(f"[Video] Frame error: {r1.stderr[-200:]}")
        return None

    print("[Video] Slideshow created ✅")

    # ── Add audio + random music ────────────────────────
    MUSIC_PATH = get_random_music()
    has_music  = MUSIC_PATH is not None

    if has_music:
        print(f"[Video] Mixing voice + music...")
        ffmpeg_final = [
            "ffmpeg", "-y",
            "-v", "quiet", "-stats",
            "-i", temp_video,
            "-i", audio_path,
            "-stream_loop", "-1", "-i", MUSIC_PATH,
            "-filter_complex",
            "[1:a]volume=1.0[voice];"
            "[2:a]volume=0.12[music];"
            "[voice][music]amix=inputs=2:duration=first[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest", "-movflags", "+faststart",
            output_path
        ]
    else:
        print("[Video] Adding voice only...")
        ffmpeg_final = [
            "ffmpeg", "-y",
            "-v", "quiet", "-stats",
            "-i", temp_video,
            "-i", audio_path,
            "-c:v", "copy", "-c:a", "aac",
            "-shortest", "-movflags", "+faststart",
            output_path
        ]

    r2 = subprocess.run(ffmpeg_final, capture_output=True, text=True)

    # ── Cleanup ─────────────────────────────────────────
    shutil.rmtree(frames_dir, ignore_errors=True)
    if os.path.exists(temp_video):
        os.remove(temp_video)

    if r2.returncode != 0:
        print(f"[Video] Audio error: {r2.stderr[-200:]}")
        return None

    print(f"[Video] Done: {output_path} ✅")
    return output_path