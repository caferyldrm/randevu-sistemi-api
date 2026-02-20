from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import models
from app.schemas import service as service_schema
from app.api.dependencies import require_admin

router = APIRouter()

# 1. LİSTELEME (Şu an gördüğün mavi buton)
@router.get("/", response_model=List[service_schema.ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()

# 2. EKLEME (Görmen gereken yeşil buton)
@router.post("/", response_model=service_schema.ServiceResponse)
def create_service(
    service: service_schema.ServiceCreate, 
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(require_admin)
):
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service