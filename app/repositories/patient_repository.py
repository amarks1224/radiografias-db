from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientRepository:
    def get_all(self, db: Session) -> list[Patient]:
        return db.query(Patient).all()

    def get_by_id(self, db: Session, patient_id: int) -> Patient | None:
        return db.query(Patient).filter(Patient.id == patient_id).first()

    def get_by_code(self, db: Session, code: str) -> Patient | None:
        return db.query(Patient).filter(Patient.code == code).first()

    def create(self, db: Session, patient_data: PatientCreate) -> Patient:
        patient = Patient(
            name=patient_data.name,
            last_name=patient_data.last_name,
            code=patient_data.code,
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

    def update(self, db: Session, patient: Patient, patient_data: PatientUpdate) -> Patient:
        update_data = patient_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(patient, field, value)

        db.commit()
        db.refresh(patient)
        return patient

    def delete(self, db: Session, patient: Patient) -> None:
        db.delete(patient)
        db.commit()

    def get_filtered(self, db: Session, name: str | None, code: str | None, order_by: str, order_dir: str, page: int, page_size: int) -> tuple[list[Patient], int]:
        query = db.query(Patient)

        if name:
            query = query.filter(Patient.name.ilike(f"%{name}%"))
        if code:
            query = query.filter(Patient.code.ilike(f"%{code}%"))

        column = getattr(Patient, order_by, Patient.id)
        if order_dir == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

        total = query.count()
        results = query.offset((page - 1) * page_size).limit(page_size).all()
        return results, total