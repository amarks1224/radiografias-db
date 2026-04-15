from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    name: str
    last_name: str
    code: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    code: str | None = None


class PatientResponse(PatientBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)