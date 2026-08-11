import sys
import argparse
import yt_dlp
import os
import subprocess
import glob
from urllib.parse import urlparse, parse_qs

def extract_cover_art(music_dir, covers_dir):
    # Ensure covers directory exists
    os.makedirs(covers_dir, exist_ok=True)

    # Find all mp3 files in the music directory
    mp3_files = glob.glob(os.path.join(music_dir, "*.mp3"))

    print(f"Found {len(mp3_files)} MP3 files. Checking covers...")

    for mp3_path in mp3_files:
        filename = os.path.basename(mp3_path)
        base_name = os.path.splitext(filename)[0]
        cover_path = os.path.join(covers_dir, f"{base_name}.jpg")
        
        # Check if cover already exists
        if os.path.exists(cover_path):
            continue

        try:
            # ffmpeg command to extract cover art
            # -i input -an (no audio) -vcodec copy (copy video stream i.e. cover) output
            cmd = [
                'ffmpeg', '-y', 
                '-loglevel', 'error',
                '-i', mp3_path, 
                '-an', 
                '-vcodec', 'copy', 
                cover_path
            ]
            subprocess.run(cmd, check=True)
            print(f"Extracted cover for: {filename}")
        except subprocess.CalledProcessError:
            # If extracting as copy fails (e.g. mjpeg inside mp3), we might just leave it 
            # or try to re-encode to jpg if strictly necessary, but 'copy' is safest for quality.
            print(f"Failed to extract cover for: {filename} (might not have embedded art)")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

def download_playlist(playlist_url, browser=None):
    # Extract playlist ID from URL
    parsed_url = urlparse(playlist_url)
    query_params = parse_qs(parsed_url.query)
    playlist_id = query_params.get('list', ['default'])[0]
    
    playlist_dir = os.path.join('downloads', playlist_id)
    music_dir = os.path.join(playlist_dir, 'music')
    covers_dir = os.path.join(playlist_dir, 'covers')
    archive_file = os.path.join(playlist_dir, 'downloaded_songs.txt')
    
    # Ensure directories exist
    os.makedirs(music_dir, exist_ok=True)
    os.makedirs(covers_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(music_dir, '%(artist|Unknown Artist).60s - %(title).100s.%(ext)s'),
        'trim_file_name': 150,
        'ignoreerrors': True,
        'download_archive': archive_file, # Track downloaded songs to avoid re-downloading
        'writethumbnail': True, 
        'extractor_args': {'youtube': {'player_client': ['web', 'mweb']}},
        'remote_components': ['ejs:github'],
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'EmbedThumbnail',
            },
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
        ],
    }

    if browser:
        print(f"Loading cookies from {browser}...")
        ydl_opts['cookiesfrombrowser'] = (browser,)

    print(f"Downloading music from: {playlist_url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
        except Exception as e:
            print(f"An error occurred: {e}")

    # Clean up loose thumbnail files in music_dir if any
    for ext in ['*.jpg', '*.webp', '*.png']:
        for f in glob.glob(os.path.join(music_dir, ext)):
            try:
                os.remove(f)
            except:
                pass

    # Extract covers
    extract_cover_art(music_dir, covers_dir)

if __name__ == "__main__":
    DEFAULT_PLAYLIST = "https://music.youtube.com/playlist?list=PL21dU0Sw564vmGlaA2Sp7Zmwpt_DwV1qY&si=6vzp7r4fwA5SHolH"
    
    parser = argparse.ArgumentParser(description="Download MP3s from a YouTube Music playlist.")
    parser.add_argument(
        "url", 
        nargs='?', 
        default=DEFAULT_PLAYLIST,
        help=f"The URL of the YouTube Music playlist (default: {DEFAULT_PLAYLIST})"
    )
    parser.add_argument(
        "--browser",
        help="Load cookies from this browser (e.g. chrome, firefox, safari) to access premium content. Ensure you are logged into YouTube Music in this browser."
    )
    
    args = parser.parse_args()
    
    download_playlist(args.url, args.browser)