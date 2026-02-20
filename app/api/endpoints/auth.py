from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import get_db
from app.core import security

router = APIRouter()

@router.post("/register")
def register(email: str, password: str, full_name: str, db: Session = Depends(get_db)):
    # Kullanıcı var mı kontrolü
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email zaten kayıtlı")
    
    hashed_pwd = security.get_password_hash(password)
    new_user = models.User(email=email, hashed_password=hashed_pwd, full_name=full_name)
    db.add(new_user)
    db.commit()
    return {"message": "Kayıt başarılı"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Hatalı email veya şifre")
    
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}