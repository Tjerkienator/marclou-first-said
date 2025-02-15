from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    youtube_api_key: str = Field(..., env='YOUTUBE_API_KEY')
    youtube_channel_id: str = Field(..., env='YOUTUBE_CHANNEL_ID')
    mongodb_uri: str = Field(..., env='MONGODB_URI')
    
    # Twitter API settings
    twitter_api_key: str = Field(..., env='TWITTER_API_KEY')
    twitter_api_secret: str = Field(..., env='TWITTER_API_SECRET')
    twitter_access_token: str = Field(..., env='TWITTER_ACCESS_TOKEN')
    twitter_access_token_secret: str = Field(..., env='TWITTER_ACCESS_TOKEN_SECRET')
    
    class Config:
        env_file = ".env" 