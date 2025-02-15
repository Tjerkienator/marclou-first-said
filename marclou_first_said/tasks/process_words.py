import asyncio
import logging
from typing import Optional

from ..services.database import DatabaseService
from ..services.word_processing import WordProcessingService

logger = logging.getLogger(__name__)

async def process_words(batch_size: Optional[int] = 10) -> int:
    """
    Process transcripts from videos and extract unique words.
    
    Args:
        batch_size: Number of videos to process in one batch
        
    Returns:
        Total number of new words found
    """
    db_service = DatabaseService()
    word_service = WordProcessingService(db_service)
    total_new_words = 0
    
    try:
        # Get unprocessed videos
        videos = await word_service.get_unprocessed_videos(limit=batch_size)
        
        if not videos:
            logger.info("No unprocessed videos found")
            return 0
        
        logger.info(f"Processing {len(videos)} videos")
        
        # Process each video
        for video in videos:
            try:
                new_words = await word_service.process_video(video)
                total_new_words += new_words
                logger.info(f"Processed video {video.video_id}: found {new_words} new words")
                
                # Add a small delay between processing videos
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing video {video.video_id}: {str(e)}")
                continue
        
        logger.info(f"Completed processing. Total new words found: {total_new_words}")
        return total_new_words
        
    except Exception as e:
        logger.error(f"Error in process_words task: {str(e)}")
        raise
    
    finally:
        db_service.client.close() 