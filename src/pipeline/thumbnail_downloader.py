import os
import requests
import pandas as pd
from pathlib import Path
import re

def safe_filename(text: str, max_len: int = 50) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")[:max_len]

def download_thumbnails(csv_path: str, output_dir: str = "data/thumbnails") -> None:
    print(f"Downloading thumbnails to {output_dir}")
    df = pd.read_csv(csv_path)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for index, row in df.iterrows():
        url = row.get("thumbnail_url")
        if not isinstance(url, str):
            continue

        title = row.get("title", "")
        safe_title = safe_filename(title)
        out_path = os.path.join(output_dir, f"{index}_{safe_title}.jpg")

        if os.path.exists(out_path):
            continue
        
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            with open(out_path, "wb") as f:
                f.write(r.content)

        except Exception as e:
            print(f"Failed to download thumbnail for row {index}: {e}")