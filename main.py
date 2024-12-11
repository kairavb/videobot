import asyncio
import uploader
import downloader

# Main function
# ----------------------------------
async def main(links):
    # Download videos
    print("Downloading videos")
    for url in links:
        downloader.download_video_by_url(url)
    
    # Monitor directory for uploads
    await uploader.monitor_directory()
# ----------------------------------

# Store links the way you wanted
# Sample links
links = [
    "https://www.instagram.com/reels/C_Lahgkt2sh/",
    "https://www.instagram.com/reels/DBJpTjko4eI/",
    "https://www.instagram.com/reels/DBRo1Mooo6E/"
]

if __name__ == "__main__":
    asyncio.run(main(links))
