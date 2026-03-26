# 🎬 YouTube Shorts Automation Project

This project is a Python-based automation tool for creating and managing YouTube Shorts. It processes media assets, generates output videos, and interacts with YouTube APIs for uploading content.

---

## 🚀 Features

- 📹 Generate YouTube Shorts automatically
- 🎵 Handle media assets (images, audio, video)
- 🔄 Modular code structure for scalability
- 🔐 Secure authentication using YouTube API
- 📂 Organized output and logging system

---

## 🛠️ Tech Stack

- Python
- YouTube Data API
- OAuth 2.0 Authentication

---

## 📁 Project Structure

Shorts/
│── assets/              # Input media files
│── logs/                # Log files
│── modules/             # Core functionality modules
│── output/              # Generated videos
│── __pycache__/         # Python cache
│── .env                 # Environment variables
│── config.py            # Configuration settings
│── main.py              # Entry point of the project
│── requirements.txt     # Dependencies
│── client_secret.json   # API credentials (ignored)
│── youtube_token.pickle # Auth token (ignored)

---

## ⚙️ Installation

1. Clone the repository:
git clone https://github.com/your-username/your-repo-name.git
cd Shorts

2. Install dependencies:
pip install -r requirements.txt

3. Set up environment variables:
Create a `.env` file and add required API keys

---

## 🔑 Setup YouTube API

1. Go to Google Cloud Console  
2. Enable YouTube Data API v3  
3. Download client_secret.json  
4. Place it in the root directory  

---

## ▶️ Usage

Run the main script:
python main.py

---

## 🔒 Security Notes

Do NOT upload:
- client_secret.json
- youtube_token.pickle
- .env

---

## 📌 Future Improvements

- Add UI dashboard
- Improve video editing pipeline
- Add scheduling system

---

## 🤝 Contributing

Pull requests are welcome.

---


