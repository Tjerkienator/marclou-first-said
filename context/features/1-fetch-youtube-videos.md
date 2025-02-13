# Fetch YouTube Video URLs

Story: As a system, I need to fetch the latest video URLs from a specific YouTube channel and store them in MongoDB to ensure we only process new videos.

Acceptance Criteria:
- Integrate with YouTube Data API v3 to fetch the latest videos.
- Extract video IDs, titles, and timestamps from the API response.
- Cross-check MongoDB to ensure the video ID does not already exist.
- If the video is new, store its details in MongoDB.
- Log successful retrieval and storage of videos for debugging purposes.
- MongoDB client should be handled in a separate file.
- the focuss lies on writing modular code.
- ensure any new packages are installed using python poetry.
- manage the init files for functions and services imports.
- manage the env variables through the dependencies.py file.