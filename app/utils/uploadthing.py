import os
import requests
from dotenv import load_dotenv

load_dotenv()

UPLOADTHING_SECRET = os.getenv("UPLOADTHING_SECRET")
UPLOADTHING_ENDPOINT = os.getenv("UPLOADTHING_ENDPOINT")

print("API KEY from ENV:", UPLOADTHING_SECRET)
print("API KEY from ENV:", UPLOADTHING_ENDPOINT)


def upload_to_uploadthing(file_path:str)-> str:
    with open(file_path, 'rb') as f:
        files = {
            "files": (os.path.basename(file_path), f, "application/octet-stream")
        }

        headers = {
            "Authorization": f"Bearer {UPLOADTHING_SECRET}"
        }

        response = requests.post(UPLOADTHING_ENDPOINT, headers=headers, files=files)
        if response.status_code== 200:
            json_resp = response.json()
            return json_resp[0]["url"]
        else:
            raise  Exception(f"UploadThing Error: {response.text}")