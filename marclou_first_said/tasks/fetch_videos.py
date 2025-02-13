import asyncio
from marclou_first_said.services import YouTubeService, DatabaseService
from marclou_first_said.config import Settings

async def fetch_new_videos():
    """Main task to fetch and store new videos"""
    settings = Settings()
    youtube = YouTubeService(settings)
    db = DatabaseService(settings)
    
    # Fetch recent videos
    videos = youtube.fetch_recent_videos()
    
    # Save to database
    await db.save_videos(videos)

if __name__ == "__main__":
    asyncio.run(fetch_new_videos()) 