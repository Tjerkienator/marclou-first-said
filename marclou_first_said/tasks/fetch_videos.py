import asyncio
import logging
from marclou_first_said.services import YouTubeService, DatabaseService

logger = logging.getLogger(__name__)

async def fetch_new_videos():
    """Main task to fetch and store new videos"""
    logger.info("Starting fetch_new_videos task")
    youtube = YouTubeService()
    db = DatabaseService()
    
    try:
        # Fetch recent videos
        logger.info("Fetching recent videos from YouTube")
        videos = youtube.fetch_recent_videos()
        logger.info(f"Found {len(videos)} recent videos")
        
        # Save to database
        logger.info("Saving videos to database")
        await db.save_videos(videos)
        logger.info("Successfully saved videos to database")
        
    except Exception as e:
        logger.error(f"Error in fetch_new_videos task: {str(e)}", exc_info=True)
        raise
    
    finally:
        if hasattr(db, 'client'):
            db.client.close()

async def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        await fetch_new_videos()
        logger.info("Task completed successfully")
    except Exception as e:
        logger.error("Task failed", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main()) 