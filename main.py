# for concurrent uploads
import asyncio

# importing uploader file
import uploader

# importing downloader file
import downloader

# importing genrator file
import genrate

# for progress bar
from tqdm import tqdm

# Main function
# ----------------------------------
async def main():
    print("0 --> genrate videos\n1 --> download videos\n2 --> monitor videos dir for upload")
    ch = int(input("enter choice: "))
    if ch == 0:
        # genrate videos
        text = input("enter text: ")
        genrate.main(text)

    elif ch == 1:
        links = []
        # Download videos
        for url in tqdm(links, desc="Downloading Videos", unit="video", leave=False):
            downloader.download_video_by_url(url)

    elif ch == 2:
        # Monitor directory for uploads
        await uploader.monitor_directory()
    
    else:
        pass
# ----------------------------------


if __name__ == "__main__":
    asyncio.run(main())
