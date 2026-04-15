from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.patient_repository import PatientRepository
from app.repositories.radiograph_repository import RadiographRepository
from app.repositories.user_repository import UserRepository
from app.schemas.radiograph import RadiographCreate, RadiographUpdate


class RadiographService:
    def __init__(self):
        self.repository = RadiographRepository()
        self.patient_repository = PatientRepository()
        self.user_repository = UserRepository()

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

    def delete_radiograph(self, db: Session, radiograph_id: int):
        radiograph = self.repository.get_by_id(db, radiograph_id)
        if not radiograph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Radiografía no encontrada"
            )

        self.repository.delete(db, radiograph)
        return {"message": "Radiografía eliminada correctamente"}