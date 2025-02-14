from motor.motor_asyncio import AsyncIOMotorClient
from marclou_first_said.models import Video
from marclou_first_said.dependencies import settings
import logging

class DatabaseService:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.mongodb_uri)
        self.db = self.client.youtube_bot
        
    async def save_videos(self, videos: list[Video]):
        """Save new videos to database if they don't exist"""
        new_count = 0
        existing_count = 0
        
        for video in videos:
            result = await self.db.videos.update_one(
                {"video_id": video.video_id},
                {"$setOnInsert": video.dict()},
                upsert=True
            )
            
            if result.upserted_id:  # Document was newly inserted
                new_count += 1
            else:  # Document already existed
                existing_count += 1
        
        logging.info(f"Processed {len(videos)} videos: {new_count} new, {existing_count} existing")
    
    async def get_unprocessed_videos(self):
        """Get videos that haven't been processed yet"""
        cursor = self.db.videos.find({"processed": False})
        return [Video(**video) async for video in cursor] 