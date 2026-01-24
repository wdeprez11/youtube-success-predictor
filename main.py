import os
from dotenv import load_dotenv

from src.pipeline.youtube_pipeline import run_pipeline
from src.models.baseline_title_model import run_baseline
from src.pipeline.thumbnail_downloader import download_thumbnails
 
def main():
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")

    df = run_pipeline(limit=200)
    log_reg = run_baseline()

    download_thumbnails("ryukahr_videos.csv")

if __name__ == "__main__":
    main()