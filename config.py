import os

# --- API Keys (set these as environment variables) ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
YOUTUBE_CLIENT_SECRET_FILE = "client_secret.json"  # from Google Cloud Console
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")   # free at pexels.com/api

# --- Channel Settings ---
NICHE = "facts and trivia"
TARGET_AUDIENCE = "general audience, all ages"
VIDEO_DURATION_SECONDS = 30
UPLOAD_HOUR = 9  # 9 AM daily post

# --- Video Settings ---
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # 9:16 Shorts format
FPS = 30
FONT_PATH = "assets/fonts/Roboto-Bold.ttf"
SUBTITLE_FONT_SIZE = 60
SUBTITLE_COLOR = "white"
SUBTITLE_BG_COLOR = "black"