import cloudinary
import cloudinary.uploader

from app.core.config import settings


cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)


class CloudinaryService:
    def upload_image(self, file_path: str):
        result = cloudinary.uploader.upload(file_path, folder="radiographs")
        return {
            "public_id": result["public_id"],
            "secure_url": result["secure_url"]
        }