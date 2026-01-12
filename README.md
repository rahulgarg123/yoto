# Yoto Music Downloader

A simple tool to download YouTube Music playlists as MP3s with high quality, embedded metadata, and separate cover art extraction. This can then be used to create MYO cards for Yoto.

## Features
- Downloads audio from YouTube/YouTube Music playlists.
- Converts to 192kbps MP3.
- Embeds thumbnails and metadata into the MP3 files.
- Automatically extracts cover art into a separate folder.
- Keeps track of downloaded songs to avoid duplicates.

## Prerequisites
- Python 3.x
- [ffmpeg](https://ffmpeg.org/) installed and in your PATH.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/rahulgarg123/yoto.git
   cd yoto
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script with a playlist URL:
```bash
python yoto_downloader.py "YOUR_PLAYLIST_URL"
```
If no URL is provided, it uses a default playlist configured in the script.

## Directory Structure
- `downloads/music/`: Contains the downloaded MP3 files.
- `downloads/covers/`: Contains the extracted cover art images.
- `downloaded_songs.txt`: Keeps track of previously downloaded URLs.