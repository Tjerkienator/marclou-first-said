import re
from typing import List, Set
from datetime import datetime

from ..models.word import Word
from ..models.video import Video
from .database import DatabaseService

class WordProcessingService:
    def __init__(self, db_service: DatabaseService):
        self.db = db_service
    
    def _normalize_word(self, word: str) -> str:
        """Normalize a word by converting to lowercase and removing punctuation."""
        # Convert to lowercase
        word = word.lower()
        # Remove punctuation and special characters
        word = re.sub(r'[^\w\s]', '', word)
        return word.strip()
    
    def _get_unique_words(self, text: str) -> Set[str]:
        """Split text into unique normalized words."""
        # Split text by spaces and normalize each word
        words = {self._normalize_word(word) for word in text.split()}
        # Remove empty strings and single characters
        return {word for word in words if len(word) > 1}
    
    async def get_unprocessed_videos(self, limit: int = 10) -> List[Video]:
        """Get videos that have transcripts but haven't been processed."""
        return await self.db.get_unprocessed_videos(limit=limit)
    
    async def process_video(self, video: Video) -> int:
        """Process a video's transcript and store new unique words."""
        if not video.transcript:
            return 0
        
        # Get unique words from transcript
        unique_words = self._get_unique_words(video.transcript)
        
        # Check which words are already in the database
        existing_words = await self.db.get_existing_words(unique_words)
        
        # Filter out existing words
        new_words = unique_words - existing_words
        
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
        
        # Mark video as processed
        await self.db.mark_video_as_processed(video.video_id)
        
        return saved_count 