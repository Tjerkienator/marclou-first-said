import re
import logging
from typing import List, Set
from datetime import datetime

from ..models.word import Word
from ..models.video import Video
from .database import DatabaseService

logger = logging.getLogger(__name__)

class WordProcessingService:
    def __init__(self, db_service: DatabaseService):
        self.db = db_service
    
    def _normalize_word(self, word: str) -> str:
        """Normalize a word by converting to lowercase and removing punctuation."""
        # Convert to lowercase
        word = word.lower()
        # Remove punctuation, special characters, and underscores
        word = re.sub(r'[^\w\s]', '', word).replace('_', '')
        return word.strip()
    
    def _get_unique_words(self, text: str) -> Set[str]:
        """Split text into unique normalized words."""
        # Split text by spaces and normalize each word
        logger.debug(f"Processing text of length: {len(text)}")
        words = {self._normalize_word(word) for word in text.split()}
        # Remove empty strings and single characters
        filtered_words = {word for word in words if len(word) > 1}
        logger.debug(f"Found {len(filtered_words)} unique words after filtering")
        return filtered_words
    
    async def get_unprocessed_videos(self, limit: int = 10) -> List[Video]:
        """Get videos that have transcripts but haven't been processed."""
        videos = await self.db.get_unprocessed_videos(limit=limit)
        logger.info(f"Retrieved {len(videos)} unprocessed videos")
        return videos
    
    async def process_video(self, video: Video) -> int:
        """Process a video's transcript and store new unique words."""
        if not video.transcript:
            logger.warning(f"Video {video.video_id} has no transcript")
            return 0
        
        # Get unique words from transcript
        logger.info(f"Extracting unique words from video {video.video_id}")
        unique_words = self._get_unique_words(video.transcript)
        logger.info(f"Found {len(unique_words)} unique words in video {video.video_id}")
        
        # Check which words are already in the database
        existing_words = await self.db.get_existing_words(unique_words)
        logger.info(f"Found {len(existing_words)} existing words in database")
        
        # Filter out existing words
        new_words = unique_words - existing_words
        logger.info(f"Found {len(new_words)} new words to save")
        
        if new_words:
            # Prepare word documents
            word_docs = [
                Word(
                    word=word,
                    video_id=video.video_id,
                    created_at=datetime.utcnow()
                )
                for word in new_words
            ]
            
            # Save new words
            saved_count = await self.db.save_words(word_docs)
            logger.info(f"Saved {saved_count} new words to database")
        else:
            saved_count = 0
            logger.info("No new words to save")
        
        # Mark video as processed
        await self.db.mark_video_as_processed(video.video_id)
        logger.info(f"Marked video {video.video_id} as processed")
        
        return saved_count 