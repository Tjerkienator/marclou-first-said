from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field

class Thumbnail(BaseModel):
    url: str
    width: int
    height: int

class Video(BaseModel):
    video_id: str = Field(..., description="YouTube video ID")
    title: str = Field(..., description="Video title")
    description: str = Field(..., description="Video description")
    published_at: datetime = Field(..., description="Video publication date")
    thumbnails: Dict[str, Thumbnail] = Field(..., description="Video thumbnails in different sizes")
    channel_title: str = Field(..., description="Channel title")
    channel_id: str = Field(..., description="Channel ID")
    tags: Optional[List[str]] = Field(default=[], description="Video tags")
    category_id: str = Field(..., description="Video category ID")
    live_broadcast_content: str = Field(..., description="Live broadcast status")
    processed: bool = Field(default=False, description="Whether video has been processed")
    processed_at: Optional[datetime] = Field(default=None, description="When video was processed")
    transcript: Optional[str] = Field(default=None, description="Video transcript text")
    transcript_fetched: bool = Field(default=False, description="Whether transcript has been fetched")
    transcript_fetched_at: Optional[datetime] = Field(default=None, description="When transcript was fetched")
    
    class Config:
        collection = "videos" 