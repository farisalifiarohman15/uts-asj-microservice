# UTS ASJ - Microservice Application

## Deskripsi Project

Project ini merupakan implementasi arsitektur **microservice** untuk memenuhi tugas **UTS Administrasi Sistem Jaringan (ASJ)**.
Aplikasi ini terdiri dari beberapa service yang berjalan menggunakan container dengan bantuan **Docker**.

Aplikasi memiliki fitur:

* Input data user
* Upload foto
* Penyimpanan data ke database
* Penyimpanan file ke object storage

## Teknologi yang Digunakan

* Python (FastAPI)
* Docker
* Docker Compose
* Nginx
* PostgreSQL
* MinIO

## Struktur Project

```
uts-asj
│
├── api
├── backend
├── frontend
├── docker-compose.yml
└── README.md
```

Penjelasan:

* **api** : service backend yang menangani request dan komunikasi dengan database
* **backend** : reverse proxy menggunakan nginx
* **frontend** : tampilan web sederhana
* **docker-compose.yml** : konfigurasi untuk menjalankan semua service
* **README.md** : dokumentasi project

## Cara Menjalankan Project

1. Clone repository

```
git clone https://github.com/farisalifiarohman15/uts-asj-microservice.git
```

2. Masuk ke folder project

```
cd uts-asj-microservice
```

3. Jalankan container

```
docker compose up -d
```

4. Cek container yang berjalan

```
docker ps
```

## Akses Aplikasi

Frontend:

```
http://localhost
```

API:

```
http://localhost:8000
```

API Documentation:

```
http://localhost:8000/docs
```

## Author

Nama : (Faris Alifia Rohman)
Mata Pelajaran : Administrasi Sistem Jaringan
Sekolah : (SMK Negeri 22 Jakarta)

