# 1. ใช้ Python เวอร์ชั่น 3.9 เป็น OS พื้นฐาน
FROM python:3.9-slim

# 2. ตั้งค่าการติดตั้ง ODBC Driver ของ Microsoft สำหรับ SQL Server (สำหรับ Debian/Linux)
RUN apt-get update && apt-get install -y curl gnupg
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# 3. สร้างพื้นที่สำหรับเก็บโค้ดใน container
WORKDIR /app

# 4. คัดลอกไฟล์ requirements.txt เข้าไปก่อน เพื่อใช้ cache ในการ build ครั้งถัดไป
COPY requirements.txt .

# 5. ติดตั้งไลบรารี Python ทั้งหมด
RUN pip install --no-cache-dir -r requirements.txt

# 6. คัดลอกโค้ดทั้งหมดของโปรเจกต์เข้าไป
COPY . .

# 7. คำสั่งที่จะให้ Render ใช้รันแอปพลิเคชันของเรา
# โดยใช้ gunicorn รันไฟล์ app.py และมองหาตัวแปร app (app:app) บน port 10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]