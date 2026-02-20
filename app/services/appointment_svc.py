# app/services/appointment_svc.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Appointment, AppointmentStatusEnum, Service
from datetime import datetime
import pytz

def create_appointment(db: Session, customer_id: str, provider_id: str, service_id: str, start_time: datetime):
    # 1. Hizmeti bul ve süresini al
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Hizmet bulunamadı")

    # Timezone Yönetimi: Frontend'den gelen tarihi UTC'ye çevirdiğimizden emin olalım
    if start_time.tzinfo is None:
        start_time = pytz.UTC.localize(start_time)
        
    # Bitiş süresini hesapla
    from datetime import timedelta
    end_time = start_time + timedelta(minutes=service.duration_minutes)

    # 2. ÇAKIŞMA KONTROLÜ (Concurrency)
    # Kural: Yeni randevunun başlangıcı, mevcut bir randevunun bitişinden ÖNCE 
    # VE yeni randevunun bitişi, mevcut randevunun başlangıcından SONRA ise çakışma vardır.
    overlapping_appointment = db.query(Appointment).filter(
        Appointment.provider_id == provider_id,
        Appointment.status != AppointmentStatusEnum.CANCELLED, # İptal edilenler çakışma yaratmaz
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    ).first()

    if overlapping_appointment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Seçilen saat diliminde personelin başka bir randevusu bulunmaktadır."
        )

    # 3. Randevuyu Oluştur
    new_appointment = Appointment(
        customer_id=customer_id,
        provider_id=provider_id,
        service_id=service_id,
        start_time=start_time,
        end_time=end_time,
        status=AppointmentStatusEnum.PENDING
    )
    
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    
    # Not: Burada Celery tetiklenip "Randevunuz alındı" maili atılabilir.
    return new_appointment