# logic.py
from googleapiclient.discovery import build
import json, os
from config import YOUTUBE_API_KEY, DATA_DIR, VIDEOS_FILE

def youtube_search(query, max_results=3):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )
    response = request.execute()
    videos = []
    for item in response.get("items", []):
        videos.append({
            "title": item["snippet"]["title"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            "thumbnail": item["snippet"]["thumbnails"]["default"]["url"]
        })
    save_videos(query, videos)
    return videos

def save_videos(query, videos):
    os.makedirs(DATA_DIR, exist_ok=True)
    data = {}
    if os.path.exists(VIDEOS_FILE):
        with open(VIDEOS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = {}
    data[query] = videos
    with open(VIDEOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
