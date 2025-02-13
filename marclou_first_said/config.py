from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    youtube_api_key: str
    youtube_channel_id: str
    mongodb_uri: str
    
    class Config:
        env_file = ".env" 