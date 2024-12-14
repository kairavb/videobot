import json
import base64
import os
import requests

# ----------------------------------
with open('genconfig.json', 'r') as file:
    config_data = json.load(file)

picAPI = config_data.get('picAPI')
vidAPI = config_data.get('vidAPI')
# ----------------------------------


def image_gen(prompt, num = 1):
    url = "https://api.freepik.com/v1/ai/text-to-image"
    # payload and headers
    # ----------------------------------
    if num > 3 or num < 1:
        return "err"
    payload = {
        "prompt": prompt,
        "negative_prompt": "b&w, cartoon, ugly",
        "guidance_scale": 2,
        "num_images": num,
        "image": {"size": "square_1_1"},
        "styling": {
            "style": "anime",
            "color": "pastel",
            "lightning": "warm",
            "framing": "portrait"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "x-freepik-api-key": picAPI
    }
    # ----------------------------------
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.text



def save_images_from_json(json_data, output_directory):
    """
    Extract Base64 images from JSON and save them to files.
    
    :param json_data: Dictionary containing the JSON data
    :param output_directory: Directory to save the images
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)
        
        # Iterate over the data items
        for idx, item in enumerate(json_data.get("data", [])):
            base64_data = item.get("base64")
            if base64_data:
                # Decode the Base64 string
                image_data = base64.b64decode(base64_data)
                
                # Save the image file
                file_path = os.path.join(output_directory, f"image_{idx + 1}.png")
                with open(file_path, "wb") as img_file:
                    img_file.write(image_data)
            else:
                print(f"No Base64 data found for item {idx + 1}")
    except Exception as e:
        print(f"Error processing images: {e}")



def generate_video_from_image(base64_image):
    """
    Sends a request to the Novita AI API to generate a video from an image.

    :param api_key: API Key for authentication.
    :param base64_image: Base64-encoded string of the image.
    :return: Response from the API.
    """
    url = "https://api.novita.ai/v3/async/img2video"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {vidAPI}"
    }
    payload = {
        "model_name": "SVD-XT",
        "image_file": base64_image,
        "frames_num": 25,
        "frames_per_second": 6,
        "seed": 20231127,
        "image_file_resize_mode": "CROP_TO_ASPECT_RATIO",
        "steps": 20,
        "motion_bucket_id": None,
        "cond_aug": None,
        "enable_frame_interpolation": False,
        "extra": {
            "response_video_type": "mp4"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Video generation initiated successfully.")
            return response.json()
        else:
            print(f"Failed to generate video: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_task_result(task_id):
    """
    Fetches the result of a task from the Novita AI API.

    :param api_key: API Key for authentication.
    :param task_id: The task ID to fetch the result for.
    :return: API response as a JSON object.
    """
    url = f"https://api.novita.ai/v3/async/task-result?task_id={task_id}"
    headers = {
        "Authorization": f"Bearer {vidAPI}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch task result: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def main(text):
    # Parse JSON string into a dictionary
    json_data = json.loads(image_gen(text, 1))
    json1 = json_data.get("data", [0])[0].get("base64")

    # Save images to the "output_images" directory
    output_dir = "./images"
    save_images_from_json(json_data, output_dir)

    print("Images genrated!\nWait 15-20s for video")

    # Call the function
    response = generate_video_from_image(json1)
    task_id = response.get("task_id")

    # vids see
    # task_id = "e0345216-3e1c-4085-afb0-bb761edd41d3"
    result = get_task_result(task_id)

    print(result["videos"][0].get("video_url"))