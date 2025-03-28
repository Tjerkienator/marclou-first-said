import tweepy
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from functools import wraps

from ..dependencies import settings
from ..models.word import Word
from .database import DatabaseService

# Rate limit decorator for Twitter API v2 Free Basic tier
def rate_limit(calls: int = 500, period: int = 30 * 24 * 3600):  # 500 tweets per 30 days
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
                    # Calculate wait time in a more human-readable format
                    hours = int(wait_time / 3600)
                    minutes = int((wait_time % 3600) / 60)
                    logging.warning(
                        f"Monthly tweet limit reached ({calls_made}/{calls} tweets). "
                        f"Will be available in {hours} hours and {minutes} minutes."
                    )
                    return False
            
            # Make the call
            calls_made += 1
            return await func(*args, **kwargs)
        return wrapper
    return decorator

class TwitterService:
    TWEETS_PER_MONTH = 500  # Twitter API v2 Free Basic tier limit
    
    def __init__(self, db_service: DatabaseService):
        self.db = db_service
        # Using Twitter API v2
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
    
    @rate_limit(calls=500, period=30 * 24 * 3600)  # 500 tweets per 30 days (Twitter API v2 Free Basic tier)
    async def tweet_word(self, word: Word) -> bool:
        """Post a word to Twitter and update its status in the database."""
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
                    reset_datetime = datetime.fromtimestamp(reset_time)
                    hours = int(wait_time / 3600)
                    minutes = int((wait_time % 3600) / 60)
                    logging.warning(
                        f"Twitter API rate limit exceeded. "
                        f"Will be available at {reset_datetime} "
                        f"(in {hours} hours and {minutes} minutes)"
                    )
            return False
        
        except tweepy.TweepyException as e:
            logging.error(f"Failed to tweet word {word.word}: {str(e)}")
            return False 