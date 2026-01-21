import os
from dotenv import load_dotenv

from src.pipeline.youtube_pipeline import run_pipeline
 
def main():
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")

    df = run_pipeline(limit=200)

if __name__ == "__main__":
    main()