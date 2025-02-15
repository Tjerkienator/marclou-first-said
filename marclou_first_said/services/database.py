from motor.motor_asyncio import AsyncIOMotorClient
from marclou_first_said.models import Video, Word
from marclou_first_said.dependencies import settings
import logging
from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.mongodb_uri)
        self.db = self.client.youtube_bot
        
    async def save_videos(self, videos: list[Video]):
        """Save new videos to database if they don't exist"""
        new_count = 0
        existing_count = 0
        
        for video in videos:
            # Initialize transcript fields for new videos
            video_data = video.dict()
            video_data.update({
                "transcript": None,
                "transcript_fetched": False,
                "transcript_fetched_at": None
            })
            
            result = await self.db.videos.update_one(
                {"video_id": video.video_id},
                {"$setOnInsert": video_data},
                upsert=True
            )
            
            if result.upserted_id:  # Document was newly inserted
                new_count += 1
            else:  # Document already existed
                existing_count += 1
        
        logging.info(f"Processed {len(videos)} videos: {new_count} new, {existing_count} existing")
    
    async def get_unprocessed_videos(self, limit: int = 10):
        """Get videos that haven't been processed yet but have transcripts"""
        cursor = self.db.videos.find({
            "transcript_fetched": True,
            "processed": False
        }).sort("published_at", 1).limit(limit)
        return [Video(**video) async for video in cursor]

    async def get_videos_without_transcript(self):
        """Get videos that don't have transcripts yet"""
        cursor = self.db.videos.find({"transcript_fetched": False})
        return [Video(**video) async for video in cursor]
    
    async def update_video_transcript(self, video_id: str, transcript: str | None):
        """Update video with transcript information"""
        await self.db.videos.update_one(
            {"video_id": video_id},
            {
                "$set": {
                    "transcript": transcript,
                    "transcript_fetched": True,
                    "transcript_fetched_at": datetime.utcnow()
                }
            }
        )
    
    async def save_words(self, words: list[Word]):
        """Save new words to database"""
        if not words:
            return 0
            
        word_docs = [word.dict() for word in words]
        result = await self.db.words.insert_many(word_docs)
        return len(result.inserted_ids)
    
    async def get_existing_words(self, words: set[str]) -> set[str]:
        """Get words that already exist in the database"""
        cursor = self.db.words.find({"word": {"$in": list(words)}})
        existing = {doc["word"] async for doc in cursor}
        return existing
    
    async def mark_video_as_processed(self, video_id: str):
        """Mark a video as processed"""
        await self.db.videos.update_one(
            {"video_id": video_id},
            {
                "$set": {
                    "processed": True,
                    "processed_at": datetime.utcnow()
                }
            }
        ) 