
## Overview

This project is a YouTube-to-Twitter Bot that monitors a specific YouTube channel, extracts transcripts from new videos, identifies unique words appearing for the first time, and tweets them. The app is deployed on Heroku and utilizes MongoDB Atlas for database storage.

## Features

- Monitor YouTube Channel – Fetches new video URLs from a target YouTube channel.
- Transcript Extraction – Retrieves video transcripts via the YouTube API.
- Word Processing – Identifies unique words from the transcript.
- Database Management – Stores processed words and videos in MongoDB.
- Twitter Posting – Tweets each new word sequentially.
- Automated Execution – Uses a scheduler (Celery/APScheduler) to run tasks periodically.

## Deployment

- Hosted on Heroku.
- Uses Heroku Scheduler (or Celery with Redis) for periodic task execution.
- MongoDB Atlas stores video data and unique words.

## API Integrations

- YouTube Data API v3 – Fetches video details and transcripts.
- Twitter API (Tweepy) – Automates tweeting of unique words.
- MongoDB Atlas – Stores processed video and word data.
