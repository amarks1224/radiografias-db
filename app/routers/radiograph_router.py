import os
import tempfile
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.models.user import User

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.db.session import get_db
from app.schemas.radiograph import (
    RadiographCreate,
    RadiographResponse,
    RadiographUpdate,
    RadiographImageUploadResponse,
)
from app.services.radiograph_service import RadiographService

router = APIRouter(prefix="/radiographs", tags=["Radiographs"])

radiograph_service = RadiographService()


@router.get("/", response_model=list[RadiographResponse])
def get_all_radiographs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return radiograph_service.get_all_radiographs(db)


@router.get("/patient/{patient_id}", response_model=list[RadiographResponse])
def get_radiographs_by_patient_id(
    patient_id: int, 
    db: Session = Depends(get_db)
    current_user: User = Depends(get_current_user)
    ):
    return radiograph_service.get_radiographs_by_patient_id(db, patient_id)


@router.get("/{radiograph_id}", response_model=RadiographResponse)
def get_radiograph_by_id(
    radiograph_id: int, 
    db: Session = Depends(get_db)
    current_user: User = Depends(get_current_user)
    ):
    return radiograph_service.get_radiograph_by_id(db, radiograph_id)


@router.post("/", response_model=RadiographResponse, status_code=201)
def create_radiograph(
    radiograph_data: RadiographCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return radiograph_service.create_radiograph(db, radiograph_data)

@router.post("/{radiograph_id}/upload-image", response_model=RadiographImageUploadResponse)
def upload_radiograph_image(
    radiograph_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    max_size = 5 * 1024 * 1024

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de archivo no permitido"
        )

    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo excede el tamaño máximo permitido de 5 MB"
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name

    try:
        return radiograph_service.upload_radiograph_image(db, radiograph_id, temp_file_path)
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.put("/{radiograph_id}", response_model=RadiographResponse)
def update_radiograph(
    radiograph_id: int,
    radiograph_data: RadiographUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return radiograph_service.update_radiograph(db, radiograph_id, radiograph_data)

@router.delete("/{radiograph_id}")
def delete_radiograph(
    radiograph_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return radiograph_service.delete_radiograph(db, radiograph_id)