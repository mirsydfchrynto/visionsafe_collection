# VisionSafe: Big Data Ingestion dan Analytics Pipeline

Project ini dibuat untuk memenuhi tugas mata kuliah Big Data. Fokus utamanya adalah melakukan pengambilan data berita kesehatan mata dari berbagai sumber terpercaya secara otomatis, menyimpannya ke database, dan melakukan analisis teks.

## Langkah Pengerjaan

1. Pengumpulan Data (Data Collection)
Sistem menggunakan script Python (data_ingestion.py) yang berjalan secara otomatis melalui GitHub Actions. Data diambil dari berbagai sumber seperti WHO, NIH, Kemenkes, dan portal berita kesehatan lainnya.

2. Penyimpanan Data (Data Storage)
Data yang telah diambil disimpan ke dalam database NoSQL yaitu Firebase Firestore. Setiap data memiliki ID unik berdasarkan URL berita untuk mencegah adanya data ganda (deduplikasi).

3. Persiapan Data (Data Preparation)
Data dari Firestore dibaca menggunakan Google Colaboratory. Tahap ini meliputi pembersihan teks dari simbol, angka, serta penghapusan kata sambung (stopwords) dalam bahasa Indonesia dan bahasa Inggris agar data siap dianalisis.

4. Analisis dan Visualisasi Data
Data yang sudah bersih divisualisasikan menggunakan grafik batang untuk melihat sebaran sumber data dan WordCloud untuk melihat tren topik kesehatan mata yang paling banyak dibahas.

## Struktur File

- data_ingestion.py: Script utama untuk mengambil data.
- requirements.txt: Daftar library Python yang dibutuhkan.
- .github/workflows/daily_sync.yml: Pengaturan jadwal otomatis harian di GitHub Actions.
- DOKUMENTASI_COLAB_BIGDATA_FIX.txt: Penjelasan teknis lengkap pengerjaan tugas.

## Cara Menjalankan Script Secara Lokal

1. Install library yang dibutuhkan:
   pip install -r requirements.txt

2. Konfigurasi Database:
   Pastikan file kredensial Firebase (serviceAccountKey.json) sudah disiapkan dan diatur dalam environment variable FIREBASE_CONFIG.

3. Jalankan script:
   python data_ingestion.py

Project ini merupakan bagian dari pengerjaan Capstone Project VisionSafe.
