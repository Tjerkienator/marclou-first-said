import tweepy
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from functools import wraps

from ..dependencies import settings
from ..models.word import Word
from .database import DatabaseService

# Rate limit decorator
def rate_limit(calls: int = 50, period: int = 3600):
    """Rate limit decorator that allows `calls` number of calls per `period` seconds."""
    def decorator(func):
        last_reset = datetime.utcnow()
        calls_made = 0
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal last_reset, calls_made
            
            # Reset counter if period has passed
            now = datetime.utcnow()
            if (now - last_reset).total_seconds() >= period:
                calls_made = 0
                last_reset = now
            
            # Check if we've hit the rate limit
            if calls_made >= calls:
                wait_time = period - (now - last_reset).total_seconds()
                if wait_time > 0:
                    logging.info(f"Rate limit reached. Waiting {wait_time:.2f} seconds")
                    await asyncio.sleep(wait_time)
                    # Reset after waiting
                    calls_made = 0
                    last_reset = datetime.utcnow()
            
            # Make the call
            calls_made += 1
            return await func(*args, **kwargs)
        return wrapper
    return decorator

class TwitterService:
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    
    def __init__(self, db_service: DatabaseService):
        self.db = db_service
        self.client = tweepy.Client(
            consumer_key=settings.twitter_api_key,
            consumer_secret=settings.twitter_api_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret
        )
        
    async def get_next_word_to_tweet(self) -> Optional[Word]:
        """Get the oldest untweeted word from the database."""
        cursor = self.db.db.words.find(
            {"tweeted": False}
        ).sort("created_at", 1).limit(1)
        
        word_doc = await cursor.to_list(length=1)
        return Word(**word_doc[0]) if word_doc else None
    
    @rate_limit(calls=50, period=3600)  # Twitter's standard rate limit: 50 tweets per hour
    async def tweet_word(self, word: Word) -> bool:
        """Post a word to Twitter and update its status in the database."""
        for attempt in range(self.MAX_RETRIES):
            try:
                # Post tweet
                tweet = self.client.create_tweet(text=word.word)
                
                # Update word status in database
                await self.db.db.words.update_one(
                    {"word": word.word},
                    {
                        "$set": {
                            "tweeted": True,
                            "tweeted_at": datetime.utcnow()
                        }
                    }
                )
                
                logging.info(f"Successfully tweeted word: {word.word}")
                return True
                
            except tweepy.TooManyRequests as e:
                reset_time = int(e.response.headers.get('x-rate-limit-reset', 0))
                if reset_time:
                    wait_time = reset_time - datetime.utcnow().timestamp()
                    if wait_time > 0:
                        logging.warning(f"Rate limit exceeded. Waiting {wait_time:.2f} seconds")
                        await asyncio.sleep(wait_time)
                        continue
                
            except tweepy.TweepyException as e:
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = self.RETRY_DELAY * (attempt + 1)  # Exponential backoff
                    logging.warning(f"Error tweeting word {word.word} (attempt {attempt + 1}/{self.MAX_RETRIES}): {str(e)}")
                    logging.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logging.error(f"Failed to tweet word {word.word} after {self.MAX_RETRIES} attempts: {str(e)}")
                    return False
        
        return False 