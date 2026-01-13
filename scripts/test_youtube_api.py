import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

CHANNEL_ID = "UCNUzWfHUP_iXZ1GMHz8gBgw"
URL = "https://www.googleapis.com/youtube/v3/search"

videos = []
next_page_token = None

while len(videos) < 100:
    params = {
        "key": API_KEY,
        "channelId": CHANNEL_ID,
        "part": "snippet",
        "order": "date",
        "maxResults": 50,
        "type": "video",
    }

    if next_page_token:
        params["pageToken"] = next_page_token

    response = requests.get(URL, params=params)
    data = response.json()

    items = data.get("items", [])
    for item in items:
        videos.append(item["id"]["videoId"])

    next_page_token = data.get("nextPageToken")

    if not next_page_token:
        break

print(f"Returned {len(videos)} videos")
print(videos[:10])

# for video in videos[:10]:
    # print(video["snippet"]["title"])
