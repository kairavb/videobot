import requests
import json
import os

# Access constants from config file
# ----------------------------------
with open('config.json', 'r') as file:
    config_data = json.load(file)

TOKEN = config_data.get('TOKEN')
UPLOAD_URL_ENDPOINT = config_data.get('UPLOAD_URL_ENDPOINT')
CREATE_POST_ENDPOINT = config_data.get('CREATE_POST_ENDPOINT')
# ----------------------------------


# Set up Header
# ----------------------------------
HEADERS = {
    "Flic-Token": TOKEN,
    "Content-Type": "application/json"
}
# ----------------------------------


def get_upload_url():
    """Fetch a pre-signed URL for video upload."""
    response = requests.get(UPLOAD_URL_ENDPOINT, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        print("Got Upload url")
        return data["url"], data["hash"]
    else:
        print(f"Failed to get upload URL: {response.status_code} - {response.text}")
        return None, None
    

def upload_video(file_path, upload_url):
    """Upload the video file to the pre-signed URL."""
    with open(file_path, "rb") as file:
        response = requests.put(upload_url, data=file)
        if response.status_code == 200:
            print(f"Video uploaded successfully: {file_path}")
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
        print(f"Post created successfully: {title}")
        return True
    else:
        print(f"Failed to create post: {response.status_code} - {response.text}")
        return False


def main():
    video_path = "./videos/vid.mp4"  # Path to video file
    video_title = "test50"  # Video title
    category_id = "Super Feed"  # Code 25 for super feed

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

    print("Process completed successfully!")


main()