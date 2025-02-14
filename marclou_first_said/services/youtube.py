from googleapiclient.discovery import build
from datetime import datetime
from typing import List, Dict
from marclou_first_said.models import Video, Thumbnail
from marclou_first_said.dependencies import settings

class YouTubeService:
    def __init__(self):
        self.api_key = settings.youtube_api_key
        self.channel_id = settings.youtube_channel_id
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def fetch_recent_videos(self, max_results: int = None) -> List[Video]:
        """
        Fetch videos from configured channel
        Args:
            max_results: Optional maximum number of videos to fetch. If None, fetches all videos.
        """
        videos = []
        next_page_token = None
        
        while True:
            request = self.youtube.search().list(
                part="snippet",
                channelId=self.channel_id,
                order="date",
                maxResults=50,  # Maximum allowed per request
                pageToken=next_page_token,
                type="video"
            )
            
            response = request.execute()
            
            for item in response['items']:
                snippet = item['snippet']
                thumbnails = {
                    size: Thumbnail(**thumb_data)
                    for size, thumb_data in snippet['thumbnails'].items()
                }
                
                video = Video(
                    video_id=item['id']['videoId'],
                    title=snippet['title'],
                    description=snippet['description'],
                    published_at=datetime.fromisoformat(
                        snippet['publishedAt'].replace('Z', '+00:00')
                    ),
                    thumbnails=thumbnails,
                    channel_title=snippet['channelTitle'],
                    channel_id=snippet['channelId'],
                    tags=snippet.get('tags', []),
                    category_id=snippet.get('categoryId', '0'),
                    live_broadcast_content=snippet['liveBroadcastContent'],
                    processed=False
                )
                videos.append(video)
            
            # Check if we've reached the requested number of videos
            if max_results and len(videos) >= max_results:
                return videos[:max_results]
            
            # Get next page token
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
                
        return videos 