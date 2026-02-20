# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from app.db.models import RoleEnum
from typing import Optional

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=3, description="Kullanıcının ad ve soyadı")
    email: EmailStr = Field(..., description="Geçerli bir e-posta adresi")
    password: str = Field(..., min_length=6, description="En az 6 karakterli şifre")
    role: Optional[RoleEnum] = Field(default=RoleEnum.CUSTOMER, description="Varsayılan olarak müşteri rolü atanır")

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str