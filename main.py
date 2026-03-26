#!/usr/bin/env python3
"""
YouTube Shorts Bot — Facts & Trivia
Runs the full pipeline: trend → script → TTS → video → upload
"""

import os
import sys
import io
import json
import logging
from datetime import datetime
from config import VIDEO_DURATION_SECONDS

# Fix Hindi encoding on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)

from modules.trending      import get_trending_topics
from modules.script_gen    import generate_script
from modules.tts           import text_to_speech
from modules.media_fetch   import fetch_pexels_images
from modules.subtitle_gen  import text_to_srt, text_to_chunks
from modules.video_compose import compose_video
from modules.uploader      import upload_short

def run_pipeline():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log.info("=" * 50)
    log.info(f"Starting pipeline run: {timestamp}")

    # ── Step 1: Get trending topic ──────────────────────
    log.info("Step 1: Fetching trending topics...")
    topics = get_trending_topics()
    topic  = topics[0] if topics else "amazing science facts"
    log.info(f"Selected topic: {topic}")

    # ── Step 2: Generate script ─────────────────────────
    log.info("Step 2: Generating script...")
    script = generate_script(topic)

    script_path = f"output/scripts/script_{timestamp}.json"
    os.makedirs("output/scripts", exist_ok=True)
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script, f, indent=2, ensure_ascii=False)

    # ── Step 3: Text-to-Speech ──────────────────────────
    log.info("Step 3: Converting to speech...")
    audio_path = f"output/audio/audio_{timestamp}.mp3"
    text_to_speech(
        script["full_script"],
        audio_path,
        voice_key="female_hindi"
    )

    # ── Step 4a: Fetch media ────────────────────────────
    log.info("Step 4a: Fetching background images...")
    search_query = script["hook"].split("!")[0].split(".")[0][:40]
    search_query = search_query.replace("Stop scrolling", "").strip()
    if not search_query:
        search_query = " ".join(script["title"].split()[:4])
    log.info("Searching images for script topic...")
    frame_dir   = f"output/frames/{timestamp}"
    image_paths = fetch_pexels_images(
        search_query,
        count=5,
        output_dir=frame_dir,
        script=script
    )

    # ── Step 4b: Generate subtitles ─────────────────────
    log.info("Step 4b: Generating subtitles...")
    subtitle_path = f"output/subtitles/sub_{timestamp}.srt"
    text_to_srt(
        script["full_script"],
        VIDEO_DURATION_SECONDS,
        subtitle_path,
        audio_path=audio_path
    )
    timed_chunks = text_to_chunks(
        script["full_script"],
        VIDEO_DURATION_SECONDS,
        audio_path=audio_path
    )

    # ── Step 5: Compose video ───────────────────────────
    log.info("Step 5: Composing final video...")
    output_path = f"output/final/short_{timestamp}.mp4"
    video = compose_video(
        image_paths=image_paths,
        audio_path=audio_path,
        subtitle_path=subtitle_path,
        output_path=output_path,
        duration=VIDEO_DURATION_SECONDS,
        timed_chunks=timed_chunks
    )

    if not video:
        log.error("Video composition failed. Aborting.")
        return False

    # ── Step 6: Upload to YouTube ───────────────────────
    log.info("Step 6: Uploading to YouTube...")
    video_id = upload_short(
        video_path=video,
        title=script["title"] + " #Shorts",
        description=script["hook"] + "\n\n" + "\n".join(script["body"]),
        hashtags=script.get("hashtags", ["#facts", "#trivia"])
    )

    log.info(f"Pipeline complete! Video ID: {video_id}")
    return True

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    success = run_pipeline()
    sys.exit(0 if success else 1)