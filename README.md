# 🚀 Profesyonel Randevu Sistemi API (Appointment System API)

Bu proje, modern web standartlarına uygun olarak geliştirilmiş, ölçeklenebilir ve güvenli bir Randevu Sistemi Backend mimarisidir. 

## 🛠️ Kullanılan Teknolojiler
* **Framework:** FastAPI (Python)
* **Veritabanı:** PostgreSQL (Neon Cloud)
* **ORM & Göç (Migration):** SQLAlchemy & Alembic
* **Güvenlik:** JWT (JSON Web Token), Bcrypt Hashing, Role-Based Access Control (Admin/Customer)
* **Konteynerleştirme:** Docker
* **Diğer:** Pydantic (Data Validation), CORS Middleware

## 💡 Temel Özellikler (Business Logic)
- **Gelişmiş Çakışma Kontrolü:** Aynı saate (Double-Booking) randevu alınmasını engelleyen algoritma.
- **Müsaitlik Hesaplama:** Personelin çalışma saatlerine ve mevcut randevularına göre boş saatleri (slot) dinamik olarak listeleme.
- **Yetkilendirme (RBAC):** Sadece 'Admin' rolündeki kullanıcıların yeni hizmet ekleyebilmesi veya silebilmesi.
- **Geçmiş Tarih Koruması:** Pydantic validator'ları ile geçmiş bir tarihe randevu alınmasının engellenmesi.
- **Güvenli Kimlik Doğrulama:** Şifrelerin Bcrypt ile hash'lenerek saklanması ve endpointlerin JWT ile korunması.

## ⚙️ Kurulum ve Çalıştırma

### Seçenek 1: Docker ile (Önerilen)
```bash
docker build -t randevu-api .
docker run -d -p 8000:8000 --env-file .env randevu-api