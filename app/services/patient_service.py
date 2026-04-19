from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self):
        self.repository = PatientRepository()

    def get_all_patients(self, db: Session):
        return self.repository.get_all(db)

    def get_patient_by_id(self, db: Session, patient_id: int):
        patient = self.repository.get_by_id(db, patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        return patient

    def create_patient(self, db: Session, patient_data: PatientCreate):
        existing_patient = self.repository.get_by_code(db, patient_data.code)
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un paciente con ese código"
            )
        return self.repository.create(db, patient_data)

    def update_patient(self, db: Session, patient_id: int, patient_data: PatientUpdate):
        patient = self.repository.get_by_id(db, patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )

        if patient_data.code:
            existing_patient = self.repository.get_by_code(db, patient_data.code)
            if existing_patient and existing_patient.id != patient_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otro paciente con ese código"
                )

        return self.repository.update(db, patient, patient_data)

    def delete_patient(self, db: Session, patient_id: int):
        patient = self.repository.get_by_id(db, patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )

        self.repository.delete(db, patient)
        return {"message": "Paciente eliminado correctamente"}

    def get_patients_filtered(self, db: Session, name: str | None, code: str | None, order_by: str, order_dir: str, page: int, page_size: int):
        results, total = self.repository.get_filtered(
            db, name, code, order_by, order_dir, page, page_size
        )
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": results
        }