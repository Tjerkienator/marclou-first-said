# Retrieve Video Transcripts

Story: As a system, I need to fetch the transcript of each new video and store it in MongoDB so that I can process the text data.

Acceptance Criteria:

- Retrieve video IDs from MongoDB that do not have a transcript.
- Use youtube_transcript_api to fetch transcripts.    
- Handle errors gracefully if transcripts are unavailable.
- Store the transcript text in MongoDB under the associated video ID.
- Mark the video document as transcript-fetched to avoid duplicate processing.
- use the existing mongodb client from anotther file.
- the focuss lies on writing modular code.