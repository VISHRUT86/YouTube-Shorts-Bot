import os
import json
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "youtube_token.pickle"

def get_youtube_service():
    """Authenticate with YouTube Data API v3 (free)."""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    
    return build("youtube", "v3", credentials=creds)

def upload_short(video_path, title, description, hashtags):
    """Upload video to YouTube as a Short."""
    youtube = get_youtube_service()
    
    # Shorts need #Shorts in description/title
    shorts_tags = hashtags + ["#Shorts", "#facts", "#trivia"]
    
    body = {
        "snippet": {
            "title": title[:100],
            "description": (
                f"{description}\n\n"
                + " ".join(shorts_tags) + "\n\n"
                + "Follow for daily mind-blowing facts! 🧠✨"
            ),
            "tags": [t.strip("#") for t in shorts_tags],
            "categoryId": "27",  # Education
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
            "madeForKids": False,
        }
    }
    
    media = MediaFileUpload(
        video_path,
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024  # 1MB chunks
    )
    
    print(f"[Upload] Uploading: {title}")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[Upload] Progress: {int(status.progress() * 100)}%")
    
    video_id = response["id"]
    print(f"[Upload] Done! https://youtube.com/shorts/{video_id}")
    return video_id