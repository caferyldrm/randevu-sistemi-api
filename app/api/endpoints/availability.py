from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db import models

router = APIRouter()

@router.get("/{date}")
def get_daily_availability(date: str, db: Session = Depends(get_db)):
    """
    Belirli bir gündeki (YYYY-MM-DD) boş randevu saatlerini döner.
    """
    # Çalışma saatleri (Örn: 09:00 - 17:00)
    start_hour = 9
    end_hour = 17
    slot_duration = 60 # 60 dakikalık slotlar
    
    # O günkü mevcut randevuları bulut veritabanından çek
    target_date = datetime.strptime(date, "%Y-%m-%d")
    appointments = db.query(models.Appointment).filter(
        models.Appointment.appointment_date >= target_date,
        models.Appointment.appointment_date < target_date + timedelta(days=1)
    ).all()
    
    occupied_slots = [a.appointment_date.strftime("%H:%M") for a in appointments]
    
    # Boş slotları hesapla
    available_slots = []
    current_time = target_date.replace(hour=start_hour, minute=0)
    
    while current_time.hour < end_hour:
        time_str = current_time.strftime("%H:%M")
        if time_str not in occupied_slots:
            available_slots.append(time_str)
        current_time += timedelta(minutes=slot_duration)
            
    return {"date": date, "available_slots": available_slots}