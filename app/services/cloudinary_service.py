import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from fastapi import HTTPException

from app.core.config import settings


cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)


class CloudinaryService:
    def upload_image(self, file_path: str):
        try:
            result = cloudinary.uploader.upload(
                file_path,
                folder="radiographs",
                type="authenticated"
            )

            return {
                "public_id": result["public_id"],
                "asset_id": result.get("asset_id"),
                "resource_type": result.get("resource_type"),
                "type": result.get("type")
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cloudinary error: {str(e)}")

    def generate_signed_url(self, public_id: str):
        url, _ = cloudinary_url(
            public_id,
            resource_type="image",
            type="authenticated",
            sign_url=True,
            secure=True
        )
        return url