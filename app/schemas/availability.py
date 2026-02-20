# app/schemas/availability.py
from pydantic import BaseModel, Field, field_validator
import re

class AvailabilityCreate(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6, description="0: Pazartesi, 6: Pazar")
    start_time: str = Field(..., description="HH:MM formatında (Örn: 09:00)")
    end_time: str = Field(..., description="HH:MM formatında (Örn: 18:00)")

    @field_validator('start_time', 'end_time')
    def validate_time_format(cls, v):
        if not re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', v):
            raise ValueError('Saat formatı HH:MM olmalıdır. Örn: 09:00')
        return v

class AvailabilityResponse(AvailabilityCreate):
    id: str
    provider_id: str
    is_active: bool

    class Config:
        from_attributes = True