from sqlalchemy.orm import Session
from datetime import date

from app.models.radiograph import Radiograph
from app.schemas.radiograph import RadiographCreate, RadiographUpdate


class RadiographRepository:
    def get_all(self, db: Session) -> list[Radiograph]:
        return db.query(Radiograph).all()

    def get_by_id(self, db: Session, radiograph_id: int) -> Radiograph | None:
        return db.query(Radiograph).filter(Radiograph.id == radiograph_id).first()

    def get_by_patient_id(self, db: Session, patient_id: int) -> list[Radiograph]:
        return db.query(Radiograph).filter(Radiograph.patient_id == patient_id).all()

    def create(self, db: Session, radiograph_data: RadiographCreate) -> Radiograph:
        radiograph = Radiograph(
            patient_id=radiograph_data.patient_id,
            user_id=radiograph_data.user_id,
            clinical_reference=radiograph_data.clinical_reference,
            study_date=radiograph_data.study_date,
            image_url=radiograph_data.image_url,
        )
        db.add(radiograph)
        db.commit()
        db.refresh(radiograph)
        return radiograph

    def update(
        self,
        db: Session,
        radiograph: Radiograph,
        radiograph_data: RadiographUpdate
    ) -> Radiograph:
        update_data = radiograph_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(radiograph, field, value)

        db.commit()
        db.refresh(radiograph)
        return radiograph
    
    def update_image_url(self, db: Session, radiograph: Radiograph, image_url: str) -> Radiograph:
        radiograph.image_url = image_url
        db.commit()
        db.refresh(radiograph)
        return radiograph

    def delete(self, db: Session, radiograph: Radiograph) -> None:
        db.delete(radiograph)
        db.commit()

    def get_filtered(self, db: Session, patient_id: int | None, is_hidden: bool | None, study_date_from: date | None, study_date_to: date | None, order_by: str, order_dir: str, page: int, page_size: int ) -> tuple[list[Radiograph], int]:
        from datetime import date as date_type
        query = db.query(Radiograph)

        if patient_id is not None:
            query = query.filter(Radiograph.patient_id == patient_id)
        if is_hidden is not None:
            query = query.filter(Radiograph.is_hidden == is_hidden)
        if study_date_from is not None:
            query = query.filter(Radiograph.study_date >= study_date_from)
        if study_date_to is not None:
            query = query.filter(Radiograph.study_date <= study_date_to)

        column = getattr(Radiograph, order_by, Radiograph.id)
        if order_dir == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

        total = query.count()
        results = query.offset((page - 1) * page_size).limit(page_size).all()
        return results, total