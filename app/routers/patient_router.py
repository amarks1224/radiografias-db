from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate, PatientListResponse
from app.services.patient_service import PatientService

from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])

patient_service = PatientService()

"""
@router.get("/", response_model=list[PatientResponse])
def get_all_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return patient_service.get_all_patients(db)
"""

@router.get("/", response_model=PatientListResponse)
def get_all_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    name: str | None = Query(default=None, description="Filtrar por nombre"),
    code: str | None = Query(default=None, description="Filtrar por código"),
    order_by: str = Query(default="id", description="Campo: id, name, last_name, created_at"),
    order_dir: str = Query(default="asc", description="Dirección: asc o desc"),
    page: int = Query(default=1, ge=1, description="Número de página"),
    page_size: int = Query(default=10, ge=1, le=100, description="Resultados por página")):

    valid_fields = {"id", "name", "last_name", "created_at"}
    if order_by not in valid_fields:
        order_by = "id"
    if order_dir not in {"asc", "desc"}:
        order_dir = "asc"

    return patient_service.get_patients_filtered(db, name, code, order_by, order_dir, page, page_size)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient_by_id(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return patient_service.get_patient_by_id(db, patient_id)


@router.post("/", response_model=PatientResponse, status_code=201)
def create_patient(
    patient_data: PatientCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return patient_service.create_patient(db, patient_data)


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return patient_service.update_patient(db, patient_id, patient_data)


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return patient_service.delete_patient(db, patient_id)

@router.get("/{patient_id}/image", response_model=PatientResponse)
def get_patient_image(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return patient_service.get_private_image(db, patient_id)

@router.get("/{patient_id}/radiographs", response_model=PatientListResponse)
def get_patient_radiographs(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    is_hidden: bool = Query(default=False, description="Filtrar por visibilidad"),
    study_date_from: str = Query(default=None, description="Fecha de estudio desde"),
    study_date_to: str = Query(default=None, description="Fecha de estudio hasta"),
    order_by: str = Query(default="id", description="Campo: id, name, last_name, created_at"),
    order_dir: str = Query(default="asc", description="Dirección: asc o desc"),
    page: int = Query(default=1, ge=1, description="Número de página"),
    page_size: int = Query(default=10, ge=1, le=100, description="Resultados por página")):

    return patient_service.get_radiographs_filtered(db, patient_id, is_hidden, study_date_from, study_date_to, order_by, order_dir, page, page_size)

