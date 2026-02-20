from pydantic import BaseModel, field_validator
from datetime import datetime
from app.db.models import AppointmentStatusEnum
from app.schemas.service import ServiceResponse # Import'u en üste aldık (PEP 8 standartı)

class AppointmentBase(BaseModel):
    service_id: int
    appointment_date: datetime

class AppointmentCreate(AppointmentBase):
    # PROFESYONEL DOKUNUŞ: Geçmiş tarihe randevu engeli
    @field_validator('appointment_date')
    @classmethod
    def date_must_be_future(cls, v: datetime):
        if v < datetime.now():
            raise ValueError('Randevu tarihi geçmiş bir zaman olamaz!')
        return v

class AppointmentResponse(AppointmentBase):
    id: int
    user_id: int
    status: AppointmentStatusEnum
    service: ServiceResponse # Randevu detayında hizmet bilgisi de gelecek

    class Config:
        from_attributes = True