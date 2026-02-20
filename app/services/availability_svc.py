# app/services/availability_svc.py
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import Availability, Appointment, AppointmentStatusEnum

def get_available_slots(db: Session, provider_id: str, target_date: date, service_duration_minutes: int):
    # 1. Personelin o gün (Haftanın günü) çalışıp çalışmadığını bul
    day_of_week = target_date.weekday() # 0: Pzt, 6: Paz
    working_hours = db.query(Availability).filter(
        Availability.provider_id == provider_id,
        Availability.day_of_week == day_of_week,
        Availability.is_active == True
    ).first()

    if not working_hours:
        return [] # O gün çalışmıyor

    # String saatleri ("09:00") datetime objesine çevir
    start_time_str = working_hours.start_time.split(":")
    end_time_str = working_hours.end_time.split(":")
    
    day_start = datetime(target_date.year, target_date.month, target_date.day, int(start_time_str[0]), int(start_time_str[1]))
    day_end = datetime(target_date.year, target_date.month, target_date.day, int(end_time_str[0]), int(end_time_str[1]))

    # 2. O günkü Onaylanmış/Bekleyen randevuları çek
    existing_appointments = db.query(Appointment).filter(
        Appointment.provider_id == provider_id,
        Appointment.status.in_([AppointmentStatusEnum.PENDING, AppointmentStatusEnum.CONFIRMED]),
        Appointment.start_time >= day_start,
        Appointment.start_time < day_end
    ).order_by(Appointment.start_time).all()

    # 3. Slotları Oluştur (Örn: 30'ar dakikalık periyotlar)
    available_slots = []
    current_time = day_start

    while current_time + timedelta(minutes=service_duration_minutes) <= day_end:
        slot_end = current_time + timedelta(minutes=service_duration_minutes)
        is_conflict = False

        # Bu slot herhangi bir randevu ile çakışıyor mu?
        for appt in existing_appointments:
            # Randevu saatlerini naive (tz-unaware) yapalım veya current_time'ı UTC yapalım (Kısa versiyon için naive varsayıyoruz)
            appt_start = appt.start_time.replace(tzinfo=None)
            appt_end = appt.end_time.replace(tzinfo=None)
            
            if (current_time < appt_end) and (slot_end > appt_start):
                is_conflict = True
                break

        if not is_conflict:
            available_slots.append({
                "start": current_time.strftime("%H:%M"),
                "end": slot_end.strftime("%H:%M")
            })

        # Bir sonraki slota geç (Örn: 30 dk sonra)
        current_time += timedelta(minutes=30) 

    return available_slots