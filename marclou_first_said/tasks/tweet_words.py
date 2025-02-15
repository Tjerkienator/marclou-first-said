import asyncio
import logging
from datetime import datetime

from ..services.database import DatabaseService
from ..services.twitter import TwitterService

async def tweet_next_word():
    """Tweet the next untweeted word from the database."""
    db_service = DatabaseService()
    twitter_service = TwitterService(db_service)
    
    # Get next word to tweet
    word = await twitter_service.get_next_word_to_tweet()
    if not word:
        logging.info("No untweeted words found in database")
        return
    
    # Tweet the word
    success = await twitter_service.tweet_word(word)
    if success:
        logging.info(f"Successfully tweeted word: {word.word}")
    else:
        logging.error(f"Failed to tweet word: {word.word}")

if __name__ == "__main__":
    asyncio.run(tweet_next_word()) 