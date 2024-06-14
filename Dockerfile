# Gunakan Python Slim sebagai base image
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Copy requirements.txt terlebih dahulu untuk memanfaatkan caching layer
COPY requirements.txt requirements.txt

# Install system dependencies yang dibutuhkan, termasuk gnupg
RUN apt-get update && apt-get install -y \
    libgomp1 \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download dan install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Download dan install ChromeDriver
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Install dependensi Python yang dibutuhkan
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi Flask ke dalam container
COPY . .

# Expose port yang digunakan oleh aplikasi (misalnya Flask)
EXPOSE 8000

# Atur environment variable untuk Flask (jika diperlukan)
ENV FLASK_APP=app.py

# Jalankan aplikasi saat container dijalankan
CMD ["flask", "run", "--host=0.0.0.0"]
