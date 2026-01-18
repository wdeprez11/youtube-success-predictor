# Youtube Video Success Predictor

This project explores whether a YouTube video will be *successful* at upload time based on available metadata, with a future goal of incorporating thumbnail image analysis.

## Project Goal

Predict whether a video will perform in the **top 25% of views** relative to other videos on the same channel.

This is framed as a **binary classification problem**:
- `1` = successful (top quartile by views)
- `0` = not successful

## Current Scope
- Collect video data using the YouTube Data API v3

## Data Source
- YouTube Data API v3
- Videos collected from a single channel (Ryukahr) for initial experimentation
- Filter out shorts (< 60 seconds)
- Label videos based on relative performance
- Save a clean, labeled dataset for modeling

## Features used (Current)
- Video title
- Video duration
- Upload time
- View count, likes, comments (for labeling only)

# Definition of "Success"
A video is considered **successful** if its view count is in the **top 25%** of videos from the same channel in the dataset.

This controls for channel size and focuses on *relative performance*

... more to be added soon