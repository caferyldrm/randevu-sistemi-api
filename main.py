# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Tüm endpointleri buraya eklemelisin
from app.api.endpoints import appointments, auth, services, availability 
from app.db.database import engine
from app.db import models

# Veritabanı tablolarını otomatik oluştur (Bulut DB bağlantısı burayı tetikler)
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Profesyonel Randevu Sistemi API",
    description="Frontend ve Backend takımları için geliştirilmiş API dokümantasyonu.",
    version="1.0.0"
)

# CORS AYARLARI
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları Sisteme Tanıtma
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(services.router, prefix="/api/v1/services", tags=["Services"])
app.include_router(availability.router, prefix="/api/v1/availability", tags=["Availability"])
app.include_router(appointments.router, prefix="/api/v1/appointments", tags=["Appointments"])

@app.get("/")
def root():
    return {
        "message": "Randevu Sistemi API'sine Hoş Geldiniz! 🚀",
        "docs_url": "/docs" 
    }