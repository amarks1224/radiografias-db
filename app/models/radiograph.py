from sqlalchemy import Integer, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date

from app.db.base import Base


class Radiograph(Base):
    __tablename__ = "radiographs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    clinical_reference: Mapped[str] = mapped_column(Text, nullable=False)
    study_date: Mapped[date] = mapped_column(Date, nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)