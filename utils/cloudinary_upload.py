import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

# print("Cloudinary Config:")
# print("CLOUD_NAME:", os.getenv("CLOUDINARY_CLOUD_NAME"))
# print("API_KEY:", os.getenv("CLOUDINARY_API_KEY"))
# print("API_SECRET:", os.getenv("CLOUDINARY_API_SECRET"))

cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

if not cloud_name or not api_key or not api_secret:
    raise Exception("Missing Cloudinary environment variables")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# To upload file to cloudinary and return the secure URL
def upload_file_to_cloudinary(file_path: str, folder="mychatcv") -> str:

    if not file_path or not os.path.exists(file_path):
        raise Exception(
            f"Cloudinary upload failed: file does not exist -> {file_path}")

    try:
        response = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            resource_type="raw",
            use_filename=False,
            unique_filename=True
        )
        return response["secure_url"]

    except Exception as e:
        raise Exception(f"Cloudinary upload failed: {str(e)}")
