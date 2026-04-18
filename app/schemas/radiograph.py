from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class RadiographBase(BaseModel):
    patient_id: int
    user_id: int
    clinical_reference: str
    study_date: date
    image_url: str


class RadiographCreate(RadiographBase):
    pass


class RadiographUpdate(BaseModel):
    patient_id: int | None = None
    user_id: int | None = None
    clinical_reference: str | None = None
    study_date: date | None = None
    image_url: str | None = None


class RadiographResponse(RadiographBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RadiographImageUploadResponse(BaseModel):
    message: str
    radiograph_id: int
    public_id: str