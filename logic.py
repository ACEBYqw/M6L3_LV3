from googleapiclient.discovery import build
import json, os
from config import YOUTUBE_API_KEY, DATA_DIR, VIDEOS_FILE

def youtube_search_single(query, max_results=3):
    """Belirli bir sorgu için YouTube'da video arar."""
    if not YOUTUBE_API_KEY:
        print("HATA: YOUTUBE_API_KEY config.py dosyasında tanımlı değil.")
        return []
        
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=max_results,
        )
        response = request.execute()
        videos = []
        for item in response.get("items", []):
            if 'videoId' not in item.get('id', {}):
                continue
                
            videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "thumbnail": item["snippet"]["thumbnails"]["default"]["url"]
            })
        return videos
    except Exception as e:
        print(f"YouTube API Hatası: {e}")
        return []

def youtube_search_comprehensive(class_name, lesson_name, topic_names):
    """
    Belirli bir sınıf ve dersin tüm konu başlıklarını arar ve sonuçlara genel tekrar videosu ekler.
    
    :param class_name: Seçilen sınıf adı (örn: "10.sınıf")
    :param lesson_name: Seçilen ders adı (örn: "Kimya")
    :param topic_names: O derse ait tüm ana konu başlıklarının listesi (örn: ["Mol Kavramı", "Asitler, Bazlar..."])
    :return: Toplam video listesi
    """
    all_videos = []
    
    for topic in topic_names:
        query = f"{class_name} {lesson_name} {topic} konu anlatımı"
        
        results = youtube_search_single(query, max_results=1) 
        
        if results:
            results[0]["title"] = f"📚 [KONU: {topic}] - " + results[0]["title"]
            all_videos.append(results[0])

    general_query = f"{class_name} {lesson_name} genel tekrar TYT AYT" 
    general_results = youtube_search_single(general_query, max_results=1)
    
    if general_results:
        general_results[0]["title"] = "🏆 [GENEL TEKRAR] - " + general_results[0]["title"]
        all_videos.append(general_results[0])

    save_videos(f"{class_name} {lesson_name} KAPSAMLI ARAMA", all_videos)
    
    return all_videos

def save_videos(query, videos):
    """Arama sonuçlarını JSON dosyasına kaydeder."""
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
