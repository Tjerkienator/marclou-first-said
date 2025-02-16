import asyncio
import logging
from marclou_first_said.services.database import DatabaseService
from marclou_first_said.services.transcript import TranscriptService

logger = logging.getLogger(__name__)

async def fetch_transcripts():
    """
    Fetch transcripts for videos that don't have them yet
    """
    logger.info("Starting fetch_transcripts task")
    db_service = DatabaseService()
    transcript_service = TranscriptService()
    
    try:
        # Get videos without transcripts
        logger.info("Fetching videos without transcripts")
        videos = await db_service.get_videos_without_transcript()
        
        if not videos:
            logger.info("No videos found without transcripts")
            return
            
        logger.info(f"Found {len(videos)} videos without transcripts")
        
        # Process each video
        for video in videos:
            try:
                logger.info(f"Fetching transcript for video {video.video_id}: {video.title}")
                transcript = await transcript_service.get_transcript(video.video_id)
                await db_service.update_video_transcript(video.video_id, transcript)
                
                status = "fetched" if transcript else "unavailable"
                logger.info(f"Transcript {status} for video {video.video_id}")
                
                # Small delay to avoid hitting API limits
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing video {video.video_id}: {str(e)}", exc_info=True)
                continue
        
        logger.info("Completed transcript fetching task")
        
    except Exception as e:
        logger.error(f"Error in fetch_transcripts task: {str(e)}", exc_info=True)
        raise
    
    finally:
        if hasattr(db_service, 'client'):
            db_service.client.close()

async def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        await fetch_transcripts()
        logger.info("Task completed successfully")
    except Exception as e:
        logger.error("Task failed", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main()) 