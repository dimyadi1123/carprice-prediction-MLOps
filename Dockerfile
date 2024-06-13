# Gunakan Python Slim sebagai base image
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Install dependensi Python yang dibutuhkan
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi Flask ke dalam container
COPY . /app

# Expose port yang digunakan oleh aplikasi (misalnya Flask)
EXPOSE 5000

# Atur environment variable untuk Flask (jika diperlukan)
ENV FLASK_APP=app.py

# Jalankan aplikasi saat container dijalankan
CMD ["flask", "run", "--host=0.0.0.0"]