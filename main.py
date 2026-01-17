import os
from dotenv import load_dotenv

from scripts.youtube_pipeline import (
    build_dataframe,
    parse_duration,
    run_pipeline
)
 
def main():
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")

    df = run_pipeline()

if __name__ == "__main__":
    main()