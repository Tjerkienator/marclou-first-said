import asyncio
import logging
from marclou_first_said.services.database import DatabaseService
from marclou_first_said.services.transcript import TranscriptService

async def fetch_transcripts():
    """
    Fetch transcripts for videos that don't have them yet
    """
    db_service = DatabaseService()
    transcript_service = TranscriptService()
    
    # Get videos without transcripts
    videos = await db_service.get_videos_without_transcript()
    if not videos:
        logging.info("No videos found without transcripts")
        return
        
    logging.info(f"Found {len(videos)} videos without transcripts")
    
    # Process each video
    for video in videos:
        transcript = await transcript_service.get_transcript(video.video_id)
        await db_service.update_video_transcript(video.video_id, transcript)
        
        status = "fetched" if transcript else "unavailable"
        logging.info(f"Transcript {status} for video {video.video_id}: {video.title}")
        
        # Small delay to avoid hitting API limits
        await asyncio.sleep(1)
    
    logging.info("Completed transcript fetching task")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run the async function
    asyncio.run(fetch_transcripts()) 