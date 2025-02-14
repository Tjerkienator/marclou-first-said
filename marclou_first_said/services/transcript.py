from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import logging
from datetime import datetime

class TranscriptService:
    async def get_transcript(self, video_id: str) -> str | None:
        """
        Fetch transcript for a YouTube video
        Returns None if transcript is unavailable
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            # Combine all transcript pieces into one text
            full_transcript = " ".join(item["text"] for item in transcript_list)
            return full_transcript
            
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            logging.warning(f"No transcript available for video {video_id}: {str(e)}")
            return None
            
        except Exception as e:
            logging.error(f"Error fetching transcript for video {video_id}: {str(e)}")
            return None 