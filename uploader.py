import requests
import json
import os
from time import sleep

# For downloafing instagram reels
import instaloader

# For downloading TikTok reels
from tiktok_downloader import snaptik

# Access constants from config file
# ----------------------------------
with open('config.json', 'r') as file:
    config_data = json.load(file)

TOKEN = config_data.get('TOKEN')
UPLOAD_URL_ENDPOINT = config_data.get('UPLOAD_URL_ENDPOINT')
CREATE_POST_ENDPOINT = config_data.get('CREATE_POST_ENDPOINT')
VIDEO_DIR = config_data.get('VIDEO_DIR')  # Directory to monitor
PROCESSED_FILES = set()  # Keep track of already processed files
# ----------------------------------


# Set up Header
# ----------------------------------
HEADERS = {
    "Flic-Token": TOKEN,
    "Content-Type": "application/json"
}
# ----------------------------------


# Handle video upload
# ----------------------------------
def get_upload_url():
    """Fetch a pre-signed URL for video upload."""
    response = requests.get(UPLOAD_URL_ENDPOINT, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data["url"], data["hash"]
    else:
        print(f"Failed to get upload URL: {response.status_code} - {response.text}")
        return None, None
    

def upload_video(file_path, upload_url):
    """Upload the video file to the pre-signed URL."""
    with open(file_path, "rb") as file:
        response = requests.put(upload_url, data=file)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to upload video: {response.status_code} - {response.text}")
            return False


def create_post(title, video_hash, category_id):
    """Create a post using the hash from the upload."""
    payload = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id
    }
    response = requests.post(CREATE_POST_ENDPOINT, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return True
    else:
        print(f"Failed to create post: {response.status_code} - {response.text}")
        return False
# ----------------------------------


# Checks every 5 seconds for new files in directory
# ----------------------------------
def monitor_directory():
    """Monitor the /videos directory for new .mp4 files."""
    global PROCESSED_FILES

    print(f"Monitoring {VIDEO_DIR} for new .mp4 files...")
    while True:
        # Get list of all .mp4 files in the directory
        current_files = {file for file in os.listdir(VIDEO_DIR) if file.endswith('.mp4')}
        
        # Identify new files by subtracting already processed files
        new_files = current_files - PROCESSED_FILES
        
        # Process new files
        for file in new_files:
            file_path = os.path.join(VIDEO_DIR, file)
            print(f"New file detected: {file_path}")
            handle_new_file(file_path)  # Call your video processing logic here

        # Update the processed files set
        PROCESSED_FILES = current_files
        
        # Sleep for a short period to avoid busy-waiting
        # Checks for every 5 seconds
        sleep(5)
# ----------------------------------


# Handle a new file discoverd by monitor
# ----------------------------------
def handle_new_file(file_path):
    video_path = f"{file_path}"  # Path to video file
    video_title = "ktest"  # Video title
    category_id = "25"  # Code 25 for super feed

    # Step 1: Fetch upload URL
    upload_url, video_hash = get_upload_url()
    if not upload_url or not video_hash:
        print("Failed to fetch upload URL. Exiting.")
        return

    # Step 2: Upload the video
    if not upload_video(video_path, upload_url):
        print("Failed to upload video. Exiting.")
        return

    # Step 3: Create the post
    if not create_post(video_title, video_hash, category_id):
        print("Failed to create post. Exiting.")
        return
    
    # Removes file after upload
    os.remove(video_path)

    print("Uploaded successfully!")
# ----------------------------------


# Download videos from instagram and tiktok with given url's
# ----------------------------------
def download_video(video_url, file_path):
    response = requests.get(video_url, stream=True)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)


def download_instagram_reel(url, save_dir="videos"):
    """
    Download an Instagram Reel with sound from the given URL.
    """
    L = instaloader.Instaloader()
    os.makedirs(save_dir, exist_ok=True)
    try:
        # Extract shortcode and fetch the post metadata
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Get the direct video URL
        video_url = post.video_url
        file_path = os.path.join(save_dir, f"{shortcode}.mp4")
        
        # Download the video with sound
        response = requests.get(video_url, stream=True)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        print(f"Instagram Reel downloaded with sound to: {file_path}")
        return file_path

    except Exception as e:
        print(f"Error downloading Instagram Reel: {e}")
        return None


def download_tiktok_video(url, save_dir="videos"):
    """
    Download an TikToks with sound from the given URL.
    """
    try:
        data = snaptik(url)
        video_url = data["download_links"][0]
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f"tiktok_{url.split('/')[-1]}.mp4")
        download_video(video_url, file_path)
        return file_path
    except:
        return None

def download_video_by_url(url):
    if "instagram.com" in url:
        return download_instagram_reel(url)
    elif "tiktok.com" in url:
        return download_tiktok_video(url)
    else:
        return None
# ----------------------------------


# Main function
# ----------------------------------
def main(links):
    for url in links:
        result = download_video_by_url(url)
        print(f"Downloaded to: {result}" if result else "Download failed.")
    monitor_directory()
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