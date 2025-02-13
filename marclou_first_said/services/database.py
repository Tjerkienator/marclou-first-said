from motor.motor_asyncio import AsyncIOMotorClient
from marclou_first_said.models import Video
from marclou_first_said.config import Settings

class DatabaseService:
    def __init__(self, settings: Settings):
        self.client = AsyncIOMotorClient(settings.mongodb_uri)
        self.db = self.client.youtube_bot
        
    async def save_videos(self, videos: list[Video]):
        """Save new videos to database if they don't exist"""
        for video in videos:
            await self.db.videos.update_one(
                {"video_id": video.video_id},
                {"$setOnInsert": video.dict()},
                upsert=True
            )
    
    async def get_unprocessed_videos(self):
        """Get videos that haven't been processed yet"""
        cursor = self.db.videos.find({"processed": False})
        return [Video(**video) async for video in cursor] 