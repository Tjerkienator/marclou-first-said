## Overview

This project is a YouTube-to-Twitter Bot that monitors a specific YouTube channel, extracts transcripts from new videos, identifies unique words appearing for the first time, and tweets them. The app is deployed on Heroku and utilizes MongoDB Atlas for database storage.

## Features

- Monitor YouTube Channel – Fetches new video URLs from a target YouTube channel.
- Transcript Extraction – Retrieves video transcripts via the YouTube API.
- Word Processing – Identifies unique words from the transcript using simple string operations.
- Database Management – Stores processed words and videos in MongoDB.
- Twitter Posting – Tweets each new word sequentially with rate limiting.
- Automated Execution – Uses Heroku Scheduler for periodic task execution.

## Deployment

- Hosted on Heroku using Poetry for dependency management.
- Uses Heroku Scheduler for independent task execution.
- Optimized for cost-efficiency with no always-on dynos.
- MongoDB Atlas stores video data and unique words.

## API Integrations

- YouTube Data API v3 – Fetches video details and transcripts.
- Twitter API (Tweepy) – Automates tweeting of unique words with rate limiting.
- MongoDB Atlas – Stores processed video and word data.
