import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from datetime import datetime

from marclou_first_said.tasks.fetch_transcripts import fetch_transcripts
from marclou_first_said.models.video import Video, Thumbnail

# Configure pytest-asyncio
pytestmark = pytest.mark.asyncio

class TestFetchTranscripts:
    @pytest.fixture
    def mock_video(self):
        """Create a mock video object for testing"""
        return Video(
            video_id="test123",
            title="Test Video",
            description="Test Description",
            published_at=datetime.utcnow(),
            thumbnails={
                "default": Thumbnail(url="http://example.com", width=120, height=90)
            },
            channel_title="Test Channel",
            channel_id="channel123",
            category_id="22",
            live_broadcast_content="none"
        )

    @pytest.fixture
    def mock_db_service(self):
        """Create a mock database service"""
        service = AsyncMock()
        service.get_videos_without_transcript = AsyncMock()
        service.update_video_transcript = AsyncMock()
        return service

    @pytest.fixture
    def mock_transcript_service(self):
        """Create a mock transcript service"""
        service = AsyncMock()
        service.get_transcript = AsyncMock()
        return service

    async def test_fetch_transcripts_success(self, mock_video, mock_db_service, mock_transcript_service):
        """Test successful transcript fetching"""
        # Setup
        mock_db_service.get_videos_without_transcript.return_value = [mock_video]
        mock_transcript_service.get_transcript.return_value = "This is a test transcript"
        
        # Patch the service classes to return our mocks
        with patch("marclou_first_said.tasks.fetch_transcripts.DatabaseService", return_value=mock_db_service), \
             patch("marclou_first_said.tasks.fetch_transcripts.TranscriptService", return_value=mock_transcript_service):
            
            # Execute
            await fetch_transcripts()
            
            # Assert
            mock_db_service.get_videos_without_transcript.assert_called_once()
            mock_transcript_service.get_transcript.assert_called_once_with(mock_video.video_id)
            mock_db_service.update_video_transcript.assert_called_once_with(
                mock_video.video_id,
                "This is a test transcript"
            )

    async def test_fetch_transcripts_no_videos(self, mock_db_service, mock_transcript_service):
        """Test behavior when no videos need transcripts"""
        # Setup
        mock_db_service.get_videos_without_transcript.return_value = []
        
        # Patch the service classes
        with patch("marclou_first_said.tasks.fetch_transcripts.DatabaseService", return_value=mock_db_service), \
             patch("marclou_first_said.tasks.fetch_transcripts.TranscriptService", return_value=mock_transcript_service):
            
            # Execute
            await fetch_transcripts()
            
            # Assert
            mock_db_service.get_videos_without_transcript.assert_called_once()
            mock_transcript_service.get_transcript.assert_not_called()
            mock_db_service.update_video_transcript.assert_not_called()

    async def test_fetch_transcripts_unavailable(self, mock_video, mock_db_service, mock_transcript_service):
        """Test handling of unavailable transcripts"""
        # Setup
        mock_db_service.get_videos_without_transcript.return_value = [mock_video]
        mock_transcript_service.get_transcript.return_value = None
        
        # Patch the service classes
        with patch("marclou_first_said.tasks.fetch_transcripts.DatabaseService", return_value=mock_db_service), \
             patch("marclou_first_said.tasks.fetch_transcripts.TranscriptService", return_value=mock_transcript_service):
            
            # Execute
            await fetch_transcripts()
            
            # Assert
            mock_db_service.get_videos_without_transcript.assert_called_once()
            mock_transcript_service.get_transcript.assert_called_once_with(mock_video.video_id)
            mock_db_service.update_video_transcript.assert_called_once_with(
                mock_video.video_id,
                None
            ) 