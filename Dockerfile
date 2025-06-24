# Gunakan base image Python yang ringan
FROM python:3.9-slim-buster

# Set working directory di dalam container
WORKDIR /app

# ---- START: TAMBAH BAGIAN INI UNTUK BUILD DEPENDENCIES ----
# Instal build dependencies yang dibutuhkan oleh mysqlclient
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*
# ---- END: TAMBAH BAGIAN INI ----

# Salin dan instal dependensi Python dari requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Salin semua isi folder proyek ke dalam container
COPY . .

# Expose port yang akan digunakan aplikasi Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi Flask (dengan hot reload)
# FLASK_APP dan FLASK_DEBUG akan diambil dari environment variables yang dimuat docker-compose
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]