from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    youtube_api_key: str = Field(..., env='YOUTUBE_API_KEY')
    youtube_channel_id: str = Field(..., env='YOUTUBE_CHANNEL_ID')
    mongodb_uri: str = Field(..., env='MONGODB_URI')
    
    class Config:
        env_file = ".env" 