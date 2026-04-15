from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.radiograph import (
    RadiographCreate,
    RadiographResponse,
    RadiographUpdate,
)
from app.services.radiograph_service import RadiographService

router = APIRouter(prefix="/radiographs", tags=["Radiographs"])

radiograph_service = RadiographService()


@router.get("/", response_model=list[RadiographResponse])
def get_all_radiographs(db: Session = Depends(get_db)):
    return radiograph_service.get_all_radiographs(db)


@router.get("/patient/{patient_id}", response_model=list[RadiographResponse])
def get_radiographs_by_patient_id(patient_id: int, db: Session = Depends(get_db)):
    return radiograph_service.get_radiographs_by_patient_id(db, patient_id)


@router.get("/{radiograph_id}", response_model=RadiographResponse)
def get_radiograph_by_id(radiograph_id: int, db: Session = Depends(get_db)):
    return radiograph_service.get_radiograph_by_id(db, radiograph_id)


@router.post("/", response_model=RadiographResponse, status_code=201)
def create_radiograph(
    radiograph_data: RadiographCreate,
    db: Session = Depends(get_db)
):
    return radiograph_service.create_radiograph(db, radiograph_data)


@router.put("/{radiograph_id}", response_model=RadiographResponse)
def update_radiograph(
    radiograph_id: int,
    radiograph_data: RadiographUpdate,
    db: Session = Depends(get_db)
):
    return radiograph_service.update_radiograph(db, radiograph_id, radiograph_data)


@router.delete("/{radiograph_id}")
def delete_radiograph(radiograph_id: int, db: Session = Depends(get_db)):
    return radiograph_service.delete_radiograph(db, radiograph_id)