import asyncio
from marclou_first_said.tasks import fetch_new_videos

async def test_fetch():
    """Simple test to verify video fetching works"""
    try:
        await fetch_new_videos()
        print("✅ Successfully fetched and stored videos!")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_fetch()) 