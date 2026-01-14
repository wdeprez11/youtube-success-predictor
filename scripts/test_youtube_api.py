import os
import requests
import re
import pandas as pd
from dotenv import load_dotenv

def parseDuration(video_time: str) -> int:
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, video_time)

    if not match:
        return 0

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    return hours * 3600 + minutes * 60 + seconds

def build_dataframe(video_data: list[dict]) -> pd.DataFrame:
    rows = []

    for item in video_data:
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        content = item.get("contentDetails", {})

        duration_seconds = parseDuration(content.get("duration", ""))

        rows.append({
            "title": snippet.get("title"),
            "published_at": snippet.get("publishedAt"),
            "duration_seconds": duration_seconds,
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
        })

    df = pd.DataFrame(rows)
    return df

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

CHANNEL_ID = "UCNUzWfHUP_iXZ1GMHz8gBgw"
URL = "https://www.googleapis.com/youtube/v3/search"

PLAYLIST_URL = "https://www.googleapis.com/youtube/v3/playlistItems"


CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"

params = {
    "key": API_KEY,
    "id": CHANNEL_ID,
    "part": "contentDetails"
}

response = requests.get(CHANNELS_URL, params=params)
data = response.json()

uploads_playlist_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

print("Uploads playlist ID:", uploads_playlist_id)

video_ids = []
next_page_token = None

while len(video_ids)  < 100:
    params = {
        "key": API_KEY,
        "playlistId": uploads_playlist_id,
        "part": "contentDetails",
        "maxResults": 50,
    }

    if next_page_token:
        params["pageToken"] = next_page_token


    response = requests.get(PLAYLIST_URL, params=params)
    data = response.json()

    for item in data.get("items", []):
        video_ids.append(item["contentDetails"]["videoId"])

    next_page_token = data.get("nextPageToken")

    if not next_page_token:
        break

print(f"Collected {len(video_ids)} video IDs")
print(video_ids[:10])

VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

video_data = []

for i in range(0, len(video_ids), 50):
    batch_ids = video_ids[i:i+50]

    params = {
        "key": API_KEY,
        "id": ",".join(batch_ids),
        "part": "snippet,statistics,contentDetails",
    }

    response = requests.get(VIDEOS_URL, params=params)
    data = response.json()

    for item in data.get("items", []):
        video_data.append(item)

print(f"Fetched metadata for {len(video_data)} videos")

df = build_dataframe(video_data)
print(df)

# sample = video_data[0]

# print(sample["snippet"]["title"])
# print(sample["statistics"]["viewCount"])
# print(sample["contentDetails"]["duration"])

# duration = parseDuration(sample["contentDetails"]["duration"])
# print(f"The video has {duration} seconds")

