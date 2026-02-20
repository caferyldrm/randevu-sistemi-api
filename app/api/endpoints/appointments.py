from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from app.db.database import get_db
from app.db import models
from app.schemas import appointment as app_schema
from app.api import dependencies

router = APIRouter()

@router.post("/", response_model=app_schema.AppointmentResponse)
def create_appointment(
    appointment: app_schema.AppointmentCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    # 1. Hizmet var mı kontrolü
    service = db.query(models.Service).filter(models.Service.id == appointment.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Hizmet bulunamadı")

    # 2. ÇAKIŞMA KONTROLÜ
    end_time = appointment.appointment_date + timedelta(minutes=service.duration_minutes)
    
    existing_appointment = db.query(models.Appointment).filter(
        models.Appointment.appointment_date < end_time,
        models.Appointment.appointment_date + timedelta(minutes=service.duration_minutes) > appointment.appointment_date,
        models.Appointment.status != models.AppointmentStatusEnum.CANCELLED
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400, 
            detail="Seçtiğiniz tarih ve saatte başka bir randevu bulunmaktadır."
        )

    # 3. Kayıt
    new_app = models.Appointment(
        **appointment.model_dump(),
        user_id=current_user.id,
        status=models.AppointmentStatusEnum.PENDING
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

@router.get("/my", response_model=List[app_schema.AppointmentResponse])
def get_my_appointments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    """Kullanıcının kendi randevularını listeler."""
    return db.query(models.Appointment).filter(models.Appointment.user_id == current_user.id).all()

@router.patch("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    """Randevuyu iptal eder."""
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id,
        models.Appointment.user_id == current_user.id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Randevu bulunamadı.")

    appointment.status = models.AppointmentStatusEnum.CANCELLED
    db.commit()
    return {"message": "Randevu iptal edildi."}