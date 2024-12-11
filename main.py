import uploader
import downloader


# Main function
# ----------------------------------
def main(links):
    for url in links:
        result = downloader.download_video_by_url(url)
        print(f"Downloaded to: {result}" if result else "Download failed.")
    uploader.monitor_directory()
# ----------------------------------

# Store links the way you wanted
# Sample links
links = [
    "https://www.instagram.com/reels/C_Lahgkt2sh/",
    "https://www.instagram.com/reels/DBJpTjko4eI/",
    "https://www.instagram.com/reels/DBRo1Mooo6E/"
]

if __name__ == "__main__":
    main(links)