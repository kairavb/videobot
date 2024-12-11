# videobot
A Python-based bot that searches, downloads, and uploads videos from social media platforms.


## Run The Project
pip install -r requirements.txt

python main.py

## Creating env
cd into directory

WINDOWS  
python -m venv venv  
.\venv\Scripts\activate

LINUX/MAC  
python -m venv myenv  
source myenv/bin/activate

## Config.json
example config file in root directory
```json
{
    "TOKEN": "your_token",
    "UPLOAD_URL_ENDPOINT": "https://api.socialverseapp.com/posts/generate-upload-url",
    "CREATE_POST_ENDPOINT": "https://api.socialverseapp.com/posts",
    "VIDEO_DIR": "./videos",
    "CATEGORY_ID": "null"
}
```