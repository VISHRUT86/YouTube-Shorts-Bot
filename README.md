
# 🎬 YouTube Shorts Automation Bot

### Automated YouTube Shorts Generation and Uploading Using Python

A Python-based automation tool designed to simplify the creation, processing, and uploading of YouTube Shorts. The project integrates media processing, workflow automation, and the **YouTube Data API v3** to reduce manual effort in managing short-form video content.

🔗 **GitHub Repository:** [YouTube Shorts Bot](https://github.com/VISHRUT86/YouTube-Shorts-Bot)

---

## 🚀 Key Features

- 📹 **Automated Video Generation:** Generate YouTube Shorts using available media assets.
- 🎵 **Media Asset Management:** Process and organize images, audio, and video files.
- ☁️ **YouTube API Integration:** Upload generated videos using YouTube Data API v3.
- 🔐 **Secure Authentication:** Implement OAuth 2.0 for authorized YouTube account access.
- 🔄 **Modular Architecture:** Organize core functionality into reusable Python modules.
- 📂 **Output Management:** Store generated videos in a dedicated output directory.
- 📝 **Logging System:** Maintain execution logs for monitoring and debugging.
- ⚙️ **Configuration Management:** Manage application settings through configuration files and environment variables.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core automation and scripting |
| YouTube Data API v3 | YouTube video uploading |
| OAuth 2.0 | Secure authentication |
| Python Modules | Modular application architecture |
| Environment Variables | Configuration and credential management |

---

## 📁 Project Structure

```text
YouTube-Shorts-Bot/
│
├── assets/                 # Input media files
├── logs/                   # Execution logs
├── modules/                # Core automation modules
├── output/                 # Generated YouTube Shorts
│
├── config.py               # Application configuration
├── main.py                 # Main entry point
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (private)
├── client_secret.json      # OAuth credentials (private)
└── youtube_token.pickle    # Authentication token (private)
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/VISHRUT86/YouTube-Shorts-Bot.git
cd YouTube-Shorts-Bot
```

### 2. Install Dependencies

Make sure Python and pip are installed.

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory.

Add the environment variables required by your application configuration.

### 4. Configure YouTube API

1. Visit [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a Google Cloud project.
3. Enable **YouTube Data API v3**.
4. Configure the OAuth consent screen.
5. Create OAuth 2.0 client credentials.
6. Download the credentials file.
7. Rename it to `client_secret.json` if necessary.
8. Place it in the project root directory.

---

## ▶️ Usage

Run the main Python script:

```bash
python main.py
```

The application executes the configured automation workflow to process media assets and generate YouTube Shorts.

YouTube uploads require valid OAuth authentication and appropriate API permissions.

---

## 🔄 Automation Workflow

```text
       Start Application
               |
               v
       Load Configuration
               |
               v
       Read Media Assets
               |
               v
       Process Video Content
               |
               v
       Generate YouTube Short
               |
               v
       Save Generated Video
               |
               v
       Authenticate YouTube API
               |
               v
       Upload Video to YouTube
               |
               v
       Log Execution Results
```

---

## 🔐 Security

This project uses OAuth 2.0 authentication for secure interaction with YouTube APIs.

### Sensitive Files

Never commit the following files to a public repository:

- `.env`
- `client_secret.json`
- `youtube_token.pickle`

### Recommended `.gitignore`

```gitignore
# Environment variables
.env

# Authentication credentials
client_secret.json
youtube_token.pickle

# Python cache
__pycache__/
*.pyc

# Virtual environment
venv/
.venv/

# Application logs
logs/*.log
```

**Important:** Never expose API credentials or authentication tokens publicly.

---

## 📈 Future Improvements

- 🌐 **Web Dashboard:** Build an interactive interface for managing Shorts.
- 📅 **Video Scheduling:** Automate video publishing at scheduled times.
- 🎞️ **Advanced Video Editing:** Improve video processing and editing capabilities.
- 🤖 **AI Integration:** Explore AI-generated scripts, captions, and metadata.
- 📊 **Analytics Dashboard:** Integrate YouTube Analytics API to monitor video performance.
- 🔁 **Batch Processing:** Support automated generation of multiple Shorts.

---

## 🤝 Contributing

Contributions and suggestions are welcome!

1. Fork the repository.
2. Create a new feature branch.

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes.

   ```bash
   git commit -m "Add new feature"
   ```

4. Push to your branch.

   ```bash
   git push origin feature/your-feature
   ```

5. Open a pull request.

---

## 👨‍💻 Developer

**Vishrut Bharti**

Indian Institute of Technology (BHU), Varanasi

- **GitHub:** [VISHRUT86](https://github.com/VISHRUT86)
- **Project Repository:** [YouTube Shorts Automation Bot](https://github.com/VISHRUT86/YouTube-Shorts-Bot)

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub!

**Made with ❤️ using Python.**
