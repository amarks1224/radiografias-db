from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_signed_radiograph_token
from app.repositories.patient_repository import PatientRepository
from app.repositories.radiograph_repository import RadiographRepository
from app.repositories.user_repository import UserRepository
from app.schemas.radiograph import RadiographCreate, RadiographUpdate
from app.services.cloudinary_service import CloudinaryService
from app.core.security import decode_signed_radiograph_token


class RadiographService:
    def __init__(self):
        self.repository = RadiographRepository()
        self.patient_repository = PatientRepository()
        self.user_repository = UserRepository()
        self.cloudinary_service = CloudinaryService()

    def get_all_radiographs(self, db: Session):
        return self.repository.get_all(db)

    def get_radiograph_by_id(self, db: Session, radiograph_id: int):
        radiograph = self.repository.get_by_id(db, radiograph_id)
        if not radiograph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Radiografía no encontrada"
            )
        return radiograph

    def get_radiographs_by_patient_id(self, db: Session, patient_id: int):
        patient = self.patient_repository.get_by_id(db, patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        return self.repository.get_by_patient_id(db, patient_id)

    def create_radiograph(self, db: Session, radiograph_data: RadiographCreate):
        patient = self.patient_repository.get_by_id(db, radiograph_data.patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )

        user = self.user_repository.get_by_id(db, radiograph_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        return self.repository.create(db, radiograph_data)

    def update_radiograph(self, db: Session, radiograph_id: int, radiograph_data: RadiographUpdate):
        radiograph = self.repository.get_by_id(db, radiograph_id)
        if not radiograph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Radiografía no encontrada"
            )

        if radiograph_data.patient_id is not None:
            patient = self.patient_repository.get_by_id(db, radiograph_data.patient_id)
            if not patient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Paciente no encontrado"
                )

        if radiograph_data.user_id is not None:
            user = self.user_repository.get_by_id(db, radiograph_data.user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )

        return self.repository.update(db, radiograph, radiograph_data)

    def upload_radiograph_image(self, db: Session, radiograph_id: int, file_path: str):
        radiograph = self.repository.get_by_id(db, radiograph_id)
        if not radiograph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Radiografía no encontrada"
            )

        upload_result = self.cloudinary_service.upload_image(file_path)
        image_public_id = upload_result["public_id"]

        updated_radiograph = self.repository.update_image_url(db, radiograph, image_public_id)

        return {
            "message": "Imagen subida correctamente como recurso protegido",
            "radiograph_id": updated_radiograph.id,
            "public_id": updated_radiograph.image_url
        }

    def delete_radiograph(self, db: Session, radiograph_id: int):
        radiograph = self.repository.get_by_id(db, radiograph_id)
        if not radiograph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Radiografía no encontrada"
            )

        self.repository.delete(db, radiograph)
        return {"message": "Radiografía eliminada correctamente"}
    
    def generate_signed_image_url(
        self,
        db: Session,
        radiograph_id: int,
        current_user_id: int,
        expires_minutes: int | None = None
    ):
        radiograph = self.repository.get_by_id(db, radiograph_id)
        if not radiograph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Radiografía no encontrada"
            )

        if not radiograph.is_hidden:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La radiografía aún no está oculta"
            )

        if radiograph.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a esta radiografía"
            )

        minutes = expires_minutes or settings.signed_url_expire_minutes

        token = create_signed_radiograph_token(
            user_id=current_user_id,
            radiograph_id=radiograph_id,
            expires_minutes=minutes
        )

        signed_url = (
            f"{settings.api_base_url}/radiographs/"
            f"{radiograph_id}/private-image?token={token}"
        )

        return {
        "radiograph_id": radiograph_id,
        "signed_url": signed_url,
        "token": token,
        "expires_in_minutes": minutes
    }

    def get_private_image(
        self,
        db: Session,
        radiograph_id: int,
        token: str
    ):
        payload = decode_signed_radiograph_token(token)

        token_radiograph_id = payload.get("radiograph_id")
        token_user_id = int(payload.get("sub"))

        if token_radiograph_id != radiograph_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El token no corresponde a esta radiografía"
            )

        radiograph = self.repository.get_by_id(db, radiograph_id)
        if not radiograph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Radiografía no encontrada"
            )

        if radiograph.user_id != token_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El token no corresponde al usuario autorizado"
            )

        if not radiograph.image_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La radiografía no tiene imagen asociada"
            )

        return self.cloudinary_service.download_protected_image(radiograph.image_url)