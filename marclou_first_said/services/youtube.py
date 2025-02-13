from googleapiclient.discovery import build
from datetime import datetime
from typing import List
from marclou_first_said.models import Video
from marclou_first_said.dependencies import settings

class YouTubeService:
    def __init__(self):
        self.api_key = settings.youtube_api_key
        self.channel_id = settings.youtube_channel_id
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def fetch_recent_videos(self, max_results: int = 10) -> List[Video]:
        """Fetch recent videos from configured channel"""
        request = self.youtube.search().list(
            part="snippet",
            channelId=self.channel_id,
            order="date",
            maxResults=max_results,
            type="video"
        )
        
        response = request.execute()
        
        videos = []
        for item in response['items']:
            video = Video(
                video_id=item['id']['videoId'],
                title=item['snippet']['title'],
                published_at=datetime.fromisoformat(
                    item['snippet']['publishedAt'].replace('Z', '+00:00')
                ),
                processed=False
            )
            videos.append(video)
            
        return videos 