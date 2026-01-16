import os
from dotenv import load_dotenv

from scripts.youtube_pipeline import (
    build_dataframe,
    parseDuration
)
 
def main():
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")

    print("Run test_youtube_api.py to generate data")

if __name__ == "__main__":
    main()