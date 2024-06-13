# Gunakan Python Slim sebagai base image
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Install dependensi sistem yang dibutuhkan
RUN apt-get update && apt-get install -y \
    libgomp1 \
    chromium \
    chromium-driver \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin \
    && chmod +x /usr/bin/chromedriver \
    && rm /tmp/chromedriver.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi Flask ke dalam container
COPY . .

# Expose port yang digunakan oleh aplikasi (misalnya Flask)
EXPOSE 5000

# Atur environment variable untuk Flask (jika diperlukan)
ENV FLASK_APP=app.py

# Jalankan aplikasi saat container dijalankan
CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["python", "-c", "from app import scheduled_scraping_job; scheduled_scraping_job()"]

