from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Word(BaseModel):
    word: str = Field(..., description="The normalized word")
    video_id: str = Field(..., description="ID of the video where the word was found")
    tweeted: bool = Field(default=False, description="Whether this word has been tweeted")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the word was first found")
    tweeted_at: Optional[datetime] = Field(default=None, description="When the word was tweeted")
    
    class Config:
        collection = "words" 