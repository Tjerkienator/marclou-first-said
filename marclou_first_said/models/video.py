from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Video(BaseModel):
    video_id: str = Field(..., description="YouTube video ID")
    title: str = Field(..., description="Video title")
    published_at: datetime = Field(..., description="Video publication date")
    processed: bool = Field(default=False, description="Whether video has been processed")
    processed_at: Optional[datetime] = Field(default=None, description="When video was processed")
    
    class Config:
        collection = "videos" 