# Menggunakan image Python sebagai base image
FROM python:3.9-slim

# Menentukan working directory di dalam container
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt .

# Menginstall dependencies yang diperlukan
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh aplikasi ke dalam container
COPY . .

# Menentukan port yang akan digunakan oleh Flask
EXPOSE 5000

# Menjalankan aplikasi Flask
CMD ["python", "app.py"]
