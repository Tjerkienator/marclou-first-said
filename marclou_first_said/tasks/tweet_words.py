import asyncio
import logging
from datetime import datetime

from ..services.database import DatabaseService
from ..services.twitter import TwitterService

logger = logging.getLogger(__name__)

async def tweet_next_word():
    """Tweet the next untweeted word from the database."""
    logger.info("Starting tweet_next_word task")
    db_service = DatabaseService()
    twitter_service = TwitterService(db_service)
    
    try:
        # Get next word to tweet
        logger.info("Fetching next word to tweet")
        word = await twitter_service.get_next_word_to_tweet()
        if not word:
            logger.info("No untweeted words found in database")
            return
        
        logger.info(f"Found word to tweet: {word.word}")
        
        # Tweet the word
        logger.info(f"Attempting to tweet word: {word.word}")
        success = await twitter_service.tweet_word(word)
        if success:
            logger.info(f"Successfully tweeted word: {word.word}")
        else:
            logger.error(f"Failed to tweet word: {word.word}")
            
    except Exception as e:
        logger.error(f"Error in tweet_next_word task: {str(e)}", exc_info=True)
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
        await tweet_next_word()
        logger.info("Task completed successfully")
    except Exception as e:
        logger.error("Task failed", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main()) 