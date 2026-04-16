from sqlalchemy.orm import Session

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