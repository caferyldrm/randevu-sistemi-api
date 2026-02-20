# 1. Python'un resmi ve hafif bir sürümünü kullanıyoruz
FROM python:3.12-slim

# 2. Çalışma dizinimizi belirliyoruz
WORKDIR /app

# 3. Önce sadece gereksinimleri kopyalıyoruz (Önbelleği verimli kullanmak için)
COPY requirements.txt .

# 4. Kütüphaneleri kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tüm proje dosyalarımızı kopyalıyoruz
COPY . .

# 6. Dış dünyaya açılacağımız port
EXPOSE 8000

# 7. Uygulamayı başlatma komutu
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]